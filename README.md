# MD7

Mail Detector 7 Day is a browser extension designed to enhance online security and reduce the risk of phishing. This extension detects the emails you are reading and the links you are about to click, providing precise alerts to fundamentally prevent phishing 🐟🐟🐟!

Using language models to analyze email text and public APIs to analyze sender information, it ensures protection for all users.

### Why Browser Extension?
You don't need to open another webpage for checking; you can see risk assessments in real-time while reading your mailbox, displayed alongside the email content. Isn't that convenient?

### Deployment
#### Run in Local
- Create a virtual environment (this needs to be done the first time, and ensure you have the `virtualenv` package)
```
virtualenv env01
```
- Execute this command in the project root directory to enter the virtual environment
```
.\env01\Scripts\activate
```
- Install packages
```
pip install -r requirements.txt
```
- Install web display and LLM interaction packages
```
pip install chainlit
pip install -U langchain-chroma
pip install -U langchain-openai
```

- Add packages
```
pip freeze > requirements.txt
```
- Set environment variables (.env). Rename `.env.example` to `.env`, and insert your own API key
- Run LLM
```
chainlit run web.py
```
## Demo
![Demo GIF](./img/Demo.gif)


## 介紹
> Power by iach526526、sharonhsuan、jameschiu1023 in AIS3 2024

>Note: Currently, you need to use your own API key and run it locally. The online version will be available soon.
