# dashboard_service/app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    user = request.args.get('user')
    return jsonify({'message': f'Welcome to your dashboard, {user}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

