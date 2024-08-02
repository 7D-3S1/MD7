import asyncio
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
from typing import List
from chainlit.element import Element
from components.VT import VT_analyze_url, VT_analyze_file

VT_API_KEY = os.getenv("VT-API-KEY")

malicious_email_vectordb = None

@cl.on_chat_start
async def start():

    global malicious_email_vectordb
    files = None

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
        malicious_email_vectordb = Chroma(persist_directory="components/malicious_email_vectordb", embedding_function=embedding)

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

    # elements = [
    #     cl.File(
    #         name="attachment",
    #         path="./input_data",
    #         display="inline",
    #         label="📎 附件上傳",
    #     )
    # ]
    # cl.user_session.set("elements", elements)

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
    # elif action.value == "attachment":
    #     await cl.Message(content="請上傳要分析的郵件附件：").send()
    #     cl.user_session.set("action", "attachment")

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
        await analyze_email(content, message.elements)
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

async def analyze_email(content, attachments: List[Element]):
    
    # 在向量數據庫中查詢最相似的 k 個向量
    k=5    
    malicious_email_vectordb = cl.user_session.get("malicious_email_vectordb")
    similar_docs = malicious_email_vectordb.similarity_search_with_score(content, k)
    print("similar_docs", similar_docs)

    if attachments:
        VT_analyze_prompt = await analyze_attachments(attachments)
    else:
        VT_analyze_prompt = ""
        
    # 準備範例文本
    examples = ""
    for doc, score in similar_docs:
        examples += f"Malicious: {doc.metadata['malicious']}\n"
        examples += f"Content: {doc.page_content}\n\n"
        print("doc=", doc.page_content, "label=", doc.metadata['malicious']," score=", score)
    # print("examples", examples)

    email_content_prompt = f"Below are the email content, and the examples are the most similar email content in the database, please refer to the examples for judgment and conclusion.\
    email_content: {content}"

    

    print("email_content_prompt", email_content_prompt)
    print("VT_analyze_prompt", VT_analyze_prompt)

    # 調用 OpenAI 模型進行分析
    runnable = cl.user_session.get("runnable")
    msg = cl.Message(content="")
    async for chunk in runnable.astream(
        {"examples": examples, "content": email_content_prompt + VT_analyze_prompt}
    ):
        await msg.stream_token(chunk)

    await msg.send()
    
    # response = await runnable.ainvoke({"examples": examples, "content": email_content_prompt + VT_analyze_prompt})

    # await cl.Message(content=f"分析結果：\n\n{response}\n\n防詐資訊：釣魚網站常常模仿知名網站的外觀，試圖騙取您的個人信息或登錄憑證。請仔細檢查URL，避免在可疑網站輸入敏感信息。").send()

async def analyze_attachments(attachments: List[Element]):
    task = [asyncio.create_task(VT_analyze_file(VT_API_KEY, attachment.path)) for attachment in attachments]
    reports = await asyncio.gather(*task)
    detect_results = []
    for report, filename in zip(reports, [attachment.name for attachment in attachments]):
        try:
            detect_results.append({
                "filename": filename,
                "antivirus_vendors_detect_type_count": {
                    "malicious": report["data"]["attributes"]["stats"]["malicious"],
                    "suspicious": report["data"]["attributes"]["stats"]["suspicious"],
                    "undetected": report["data"]["attributes"]["stats"]["undetected"],
                    "harmless": report["data"]["attributes"]["stats"]["harmless"],
                }
            })
        except Exception as e:
            print(f"Error: {e}")
            detect_results.append(None)

    VT_analyze_prompt = f"Additionally, we have the results of the antivirus analysis of the files attached to the email, the item antivirus_vendors_detect_type_count is the number of antivirus vendors have scanned, which contains four items, malicious files, suspicious files, undetected suspicious files, and harmless files. Please also refer to this analysis result for judgment and conclusion.\
    reports: {detect_results}"

    return VT_analyze_prompt

# 需要再修改內容
def check_suspicious_content(content):
    suspicious_keywords = ['密碼', '信用卡', '緊急', '中獎', '錢']
    return any(keyword in content for keyword in suspicious_keywords)

if __name__ == "__main__":
    cl.run()