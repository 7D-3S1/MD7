import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
# from web import analyze_email
load_dotenv(f'{os.getcwd()}\.env')
api_KEY = os.getenv('hunterIO')
#問題還很多，不要用
app = FastAPI()

@app.get("/analyzeSender/{Sender}")
async def analyze_email_route(Sender: str):
    url = f'https://api.hunter.io/v2/email-verifier?email={Sender}&api_key={api_KEY}'

    # 發送請求
    try:
        response = requests.get(url)
        if response.status_code == 200:
        # 解析 JSON
            data = response.json()
            # print(json.dumps(data, indent=4))# for debug
            return data
        elif response.status_code == 202:
            print(f'fail check sender_credit 過一陣子再試一次: {response.status_code}, 錯誤 {response.text}')
            return [-202]
        else:
            print(f'fail check sender_credit: {response.status_code}, 錯誤: {response.text}')
            return [-400]
    except requests.exceptions.RequestException as e:
        print('Fail due to check sender_credit:',e)
        return [-500]
    
    # return {"content": content, "attachments": attachments}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)
    
    
