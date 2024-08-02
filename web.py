import chainlit as cl
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import numpy as np
import components as comp

load_dotenv('components/.env')
openai_api_key = os.getenv("OPENAI_API_KEY")

malicious_email_vectordb = None

@cl.on_chat_start
async def start():

    global malicious_email_vectordb

    # 模型初始化，設置 model 版本與 streaming=True 以支持逐步獲取回應
    model = ChatOpenAI(
        model_name="gpt-4",
        streaming=True
    )
    prompt = ChatPromptTemplate.from_messages(
        [   ("system", "You are an expert in cybersecurity and phishing detection. Analyze the given content and provide detailed insights on whether it's suspicious or not. If it's suspicious, explain why and provide safety tips.\
            **Output in Traditional Chinese**"),
            ("human", "{content}"),
        ]
    )
    
    # 初始化一個與預先訓練好的向量資料庫相同的Embadding model
    embedding = OpenAIEmbeddings()
    # 將預先訓練好的向量資料庫連接到持久化目錄
    if malicious_email_vectordb is None:
        malicious_email_vectordb = Chroma(persist_directory="components\malicious_email_vectordb", embedding_function=embedding)

    runnable = prompt | model | StrOutputParser()

    # 將所需組件儲存在user session中
    cl.user_session.set("malicious_email_vectordb", malicious_email_vectordb)
    cl.user_session.set("runnable", runnable)
    cl.user_session.set("embedding", embedding)

    actions = [
        # cl.Action(name="action", value="Website", label="✅ Website"),
        # cl.Action(name="action", value="SMS", label="✅ SMS"),
        cl.Action(name="action", value="Email", label="✅ Email"),
    ]
    cl.user_session.set("actions", actions)

    msg = cl.Message(
        content="歡迎使用防詐小精靈! 請選擇要分析的內容類型：",
        actions=actions,
    )
    await msg.send()

@cl.action_callback("action")
async def on_action(action: cl.Action):
    # print("hi", action.forId)
    if action.value == "Website":
        await cl.Message(content="請輸入要分析的網頁 URL：").send()
        cl.user_session.set("action", "url")
    elif action.value == "SMS":
        await cl.Message(content="請輸入要分析的簡訊內容：").send()
        cl.user_session.set("action", "SMS")
    elif action.value == "Email":
        await cl.Message(content="請輸入要分析的郵件內容：").send()
        cl.user_session.set("action", "Email")

@cl.on_message
async def main(message: cl.Message):
    action = cl.user_session.get("action")
    content = message.content
    print(action, content)
    if action == "url":
        await analyze_url(content)
    elif action == "SMS":
        await analyze_sms(content)
    elif action == "Email":
        await analyze_email(content)
    else:
        await cl.Message(content="請先選擇要分析的內容類型。").send()


async def analyze_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        suspicious = check_suspicious_content(soup.text)
        
        if suspicious:
            result = "該網址可能是釣魚網站。請小心！"
        else:
            result = "該網址暫時沒有發現明顯的釣魚特徵，但仍需謹慎。"
        
        await cl.Message(content=f"分析結果：{result}\n\n防詐資訊：釣魚網站常常模仿知名網站的外觀，試圖騙取您的個人信息或登錄憑證。請仔細檢查URL，避免在可疑網站輸入敏感信息。").send()
    
    except Exception as e:
        await cl.Message(content=f"無法分析該URL: {str(e)}").send()

async def analyze_sms(content):
    suspicious = check_suspicious_content(content)
    
    if suspicious:
        result = "該簡訊內容可能是釣魚詐騙。請小心！"
    else:
        result = "該簡訊內容暫時沒有發現明顯的釣魚特徵，但仍需謹慎。"
    
    await cl.Message(content=f"分析結果：{result}\n\n防詐資訊：釣魚簡訊常常聲稱來自銀行或其他機構，要求您提供個人信息或點擊可疑鏈接。請不要回覆可疑簡訊或點擊其中的鏈接。").send()

async def analyze_email(content):

    # 在向量數據庫中查詢最相似的 k 個向量
    k=5    
    malicious_email_vectordb = cl.user_session.get("malicious_email_vectordb")
    similar_docs = malicious_email_vectordb.similarity_search_with_score(content, k)

    # 準備範例文本
    examples = ""
    for doc, score in similar_docs:
        examples += f"Content: {doc.page_content}\n"
        examples += f"Malicious: {doc.metadata['malicious']}\n\n"
        print("doc=", doc.page_content, "label=", doc.metadata['malicious']," score=", score)
    print("examples", examples)

    runnable = cl.user_session.get("runnable")
    response = await runnable.ainvoke({"examples": examples, "content": content})

    await cl.Message(content=f"分析結果：\n\n{response}\n\n防詐資訊：釣魚網站常常模仿知名網站的外觀，試圖騙取您的個人信息或登錄憑證。請仔細檢查URL，避免在可疑網站輸入敏感信息。").send()

# 需要再修改內容
def check_suspicious_content(content):
    suspicious_keywords = ['密碼', '信用卡', '緊急', '中獎', '錢']
    return any(keyword in content for keyword in suspicious_keywords)

if __name__ == "__main__":
    cl.run()