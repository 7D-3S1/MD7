from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from components.detect import mailStatus
app = Flask(__name__)
CORS(app)
api_KEY = os.getenv('HUNTER_IO_API_KEY')

@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'No email provided'}), 400
    return mailStatus(email)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
