import chainlit as cl
import requests
import re
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

# 假設你已經有一個惡意網址資料庫，並已經將其轉換為向量存儲在 Chroma 中
# 這裡我們先創建一個示例數據庫
malicious_data = [
    ("This is a phishing website trying to steal your credentials.", True),
    ("Welcome to our legitimate online store.", False),
    ("Your account has been locked. Click here to verify your identity.", True),
    ("Thank you for visiting our official website.", False),
    ("Congratulations! You've won a prize. Enter your details to claim.", True),
]

# 初始化 OpenAI 嵌入模型
embeddings = OpenAIEmbeddings()

# 創建向量數據庫
texts = [text for text, _ in malicious_data]
metadatas = [{"malicious": label} for _, label in malicious_data]
vectordb = Chroma.from_texts(texts, embeddings, metadatas=metadatas, persist_directory="malicious_email_vectordb")
