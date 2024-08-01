import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(f'{os.getcwd()}\mail\.env')
api_KEY = os.getenv('ipqualityscore')
# 現在缺少可用的免費API服務
email_to_check = 'service@ais3.org'

# 設定API網址
url = f'https://www.ipqualityscore.com/api/json/email/{api_KEY}/{email_to_check}'

# 發送請求
response = requests.get(url)

# 檢查response狀態
if response.status_code == 200:
    # 解析 JSON 数据
    data = response.json()
    print(json.dumps(data, indent=4))
else:
    print(f'请求失败，状态码: {response.status_code}, 错误信息: {response.text}')