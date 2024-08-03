# Day 7 Project

D7 計畫，七天內生出一個酷酷的專案。我想做瀏覽器插件！！
## 所以這是什麼東西？
這是在 AIS3 2024 生出的小專案，由 iach526526、sharonhsuan、jameschiu1023 共同開發。

### why 瀏覽器插件
比一般網頁的方式呈現還要新穎，泛用性更高，使用者不需要開另一個網頁去檢查，打開信箱就可以即時看到風險評估
### 執行
- 建立虛擬環境(第一次執行需要執行，並確保有 virtualenv 套件)
```
virtualenv env01
```
- 在專案跟目錄執行此命令進入虛擬環境
```
.\env01\Scripts\activate
```
- 安裝套件
```
pip install -r requirements.txt
```
- 安裝網頁顯示與LLM互動套件
```
pip install chainlit
pip install -U langchain-chroma
pip install -U langchain-openai
```

- 增加套件
```
pip freeze > requirements.txt
```
```
chainlit run web.py
```
- 設定環境變數(.env)



