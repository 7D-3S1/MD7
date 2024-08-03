from flask import Flask, request, jsonify
import os
import json
from flask_cors import CORS
from components.detect import sender_credit
from components.VT import VT_analyze_url
app = Flask(__name__)
CORS(app)
api_KEY = os.getenv('HUNTER_IO_API_KEY')

@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'No email provided'}), 400
    res=sender_credit(email)
    print("/check_email type",type(res))
    return res
@app.route('/url_check', methods=['POST'])
async def url_check():
    url = request.json.get('url')
    print(url)
    print("analyzing url: ",url)
    res=await VT_analyze_url(url)
    print("app route:",json.dumps(res, indent=4))
    return res
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
