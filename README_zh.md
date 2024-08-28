# MD7

Mail Detector 7 Day 是一個瀏覽器擴充套件，專為加強網路安全和減少被網路釣魚。這個擴充套件檢測正在閱讀的電子郵件和即將點閱的連結，給出精確的提醒，從根本預防網路釣魚🐟🐟🐟！

使用語言模型分析郵件文本、公開 API 分析寄件訊息，為所有使用者做好把關



### why 瀏覽器擴充套件？
不需要開另一個網頁去檢查，閱讀信箱時就可以即時看到風險評估，和郵件內容一起顯示，不香嗎？


### 部屬
#### run in local
- 建立虛擬環境(第一次執行需要執行，並確保有 virtualenv 套件)

virtualenv env01


- 在專案跟目錄執行此命令進入虛擬環境

.\env01\Scripts\activate


- 安裝套件

pip install -r requirements.txt


- 安裝網頁顯示與LLM互動套件

pip install chainlit
pip install -U langchain-chroma
pip install -U langchain-openai



- 增加套件

pip freeze > requirements.txt


- 設定環境變數(.env)，把 .env.example 改檔名為 .env，並把你自己的 API key 塞進去
- Run LLM

chainlit run web.py


## Demo
![Demo GIF](./img/Demo.gif)

## 介紹
> 這是在 AIS3 2024 在七天內誕生的小專案，由 iach526526、sharonhsuan、jameschiu1023 共同開發。

