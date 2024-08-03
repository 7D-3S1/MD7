from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import pandas as pd
# 初始化 OpenAI 嵌入模型
embeddings = OpenAIEmbeddings(show_progress_bar=True)

file_path = 'components/train_spam.csv'
csv_data = pd.read_csv(file_path)
texts = csv_data['v2'].tolist()
metadatas = [{"malicious": label} for label in csv_data['v1'].tolist()]
print(texts[:5])
print(metadatas[:5])
# input("Press Enter to continue...")
# chunked the data into smaller pieces to avoid memory issues in Chroma
CHUNK_SIZE = 100

vectordb = Chroma.from_texts(texts[:CHUNK_SIZE], embeddings, metadatas=metadatas[:CHUNK_SIZE], persist_directory="components/malicious_email_vectordb")

for i in range(CHUNK_SIZE, len(texts), CHUNK_SIZE):
    chunk_texts = texts[i:i+CHUNK_SIZE]
    chunk_metadatas = metadatas[i:i+CHUNK_SIZE]
    vectordb.add_texts(chunk_texts, metadatas=chunk_metadatas)