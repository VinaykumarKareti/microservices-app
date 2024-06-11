# frontend/app.py
from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'anothersecretkey'

auth_service_url = 'http://auth_service:5000'
dashboard_service_url = 'http://dashboard_service:5001'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{auth_service_url}/login', json={'username': username, 'password': password})
        if response.status_code == 200:
            session['user'] = username
            return redirect(url_for('dashboard'))
        return response.json()['message']
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{auth_service_url}/signup', json={'username': username, 'password': password})
        return response.json()['message']
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = session['user']
        response = requests.get(f'{dashboard_service_url}/dashboard', params={'user': user})
        return render_template('dashboard.html', message=response.json()['message'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    requests.post(f'{auth_service_url}/logout')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

