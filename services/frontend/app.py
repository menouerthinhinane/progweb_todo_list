from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
import requests
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'votre-secret-key-tres-secrete')

# IMPORTANT: Utiliser localhost pour le développement local !
USERS_URL = os.environ.get('USERS_URL', 'http://localhost:5001')
TASKS_URL = os.environ.get('TASKS_URL', 'http://localhost:5002')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# Pages
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

# API Routes
@app.route('/api/users', methods=['POST'])
def proxy_register():
    try:
        resp = requests.post(f'{USERS_URL}/users', json=request.get_json(), timeout=5)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/login', methods=['POST'])
def proxy_login():
    try:
        resp = requests.post(f'{USERS_URL}/users/login', json=request.get_json(), timeout=5)
        data = resp.json()
        if resp.status_code == 200:
            session['user_id'] = data['id']
            session['username'] = data['username']
            session['token'] = data.get('token')  # Utilise get car le token peut ne pas exister
        return jsonify(data), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['GET', 'POST'])
@login_required
def proxy_tasks():
    headers = {}
    if session.get('token'):
        headers['Authorization'] = f'Bearer {session["token"]}'
    
    try:
        if request.method == 'GET':
            # Ajoute user_id en paramètre
            resp = requests.get(
                f'{TASKS_URL}/tasks?user_id={session["user_id"]}', 
                headers=headers, 
                timeout=5
            )
        else:  # POST
            data = request.get_json()
            data['user_id'] = session['user_id']  # Ajoute automatiquement user_id
            resp = requests.post(
                f'{TASKS_URL}/tasks', 
                json=data, 
                headers=headers, 
                timeout=5
            )
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
@login_required
def proxy_task_detail(task_id):
    headers = {}
    if session.get('token'):
        headers['Authorization'] = f'Bearer {session["token"]}'
    
    try:
        if request.method == 'PUT':
            resp = requests.put(
                f'{TASKS_URL}/tasks/{task_id}', 
                json=request.get_json(), 
                headers=headers, 
                timeout=5
            )
        else:  # DELETE
            resp = requests.delete(
                f'{TASKS_URL}/tasks/{task_id}', 
                headers=headers, 
                timeout=5
            )
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Déconnecté'})

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)