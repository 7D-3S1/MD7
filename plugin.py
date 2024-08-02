from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from components.detect import mailStatus
app = Flask(__name__)
CORS(app)
api_KEY = os.getenv('HUNTER_IO_API_KEY')

counter = 0
@app.route('/check_email', methods=['POST'])
def check_email():
    global counter#for debug
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'No email provided'}), 400
    res=mailStatus(email)
    print("/check_email  -------------",counter);counter+=1
    return res
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
