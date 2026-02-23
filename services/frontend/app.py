from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
import requests
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'votre-secret-key-tres-secrete'

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://users:5001')

# Décorateur pour vérifier l'authentification
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# Routes pour les pages
@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    registered = request.args.get('registered', False)
    if registered:
        flash('Inscription réussie ! Vous pouvez vous connecter.', 'success')
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/tasks')
@login_required
def tasks_page():
    return render_template('tasks.html', username=session.get('username'))

# Routes API (proxy vers le backend)
@app.route('/api/users/register', methods=['POST'])
def proxy_register():
    try:
        resp = requests.post(
            f'{BACKEND_URL}/users',
            json=request.get_json(),
            timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/login', methods=['POST'])
def proxy_login():
    try:
        resp = requests.post(
            f'{BACKEND_URL}/users/login',
            json=request.get_json(),
            timeout=5
        )
        data = resp.json()
        if resp.status_code == 200:
            session['user_id'] = data['id']
            session['username'] = data['username']
        return jsonify(data), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['GET', 'POST'])
@login_required
def proxy_tasks():
    headers = {'Authorization': request.headers.get('Authorization', '')}
    user_id = session.get('user_id')
    
    try:
        if request.method == 'GET':
            resp = requests.get(
                f'{BACKEND_URL}/tasks?user_id={user_id}',
                headers=headers,
                timeout=5
            )
        else:
            data = request.get_json()
            data['user_id'] = user_id
            resp = requests.post(
                f'{BACKEND_URL}/tasks',
                json=data,
                headers=headers,
                timeout=5
            )
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)