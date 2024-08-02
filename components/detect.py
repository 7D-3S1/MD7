import os
import requests
import json
from dotenv import load_dotenv
load_dotenv(f'{os.getcwd()}\components\.env')
api_KEY = os.getenv('hunterIO')


def sender_credit(email):
    # hunter.io 最高！！
    url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_KEY}'

    # 發送請求
    try:
        response = requests.get(url)
        if response.status_code == 200:
        # 解析 JSON 数据
            data = response.json()
            print(json.dumps(data, indent=4))# for debug
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
    # 檢查response狀態