from flask import Flask, request, jsonify
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )

def init_db():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    password_hash VARCHAR(200) NOT NULL
                )
            ''')
init_db()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing fields'}), 400
    pwd_hash = generate_password_hash(password)
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO users (username, password_hash) VALUES (%s,%s) RETURNING id',
                            (username, pwd_hash))
                user_id = cur.fetchone()[0]
        return jsonify({'id': user_id, 'username': username}), 201
    except psycopg2.IntegrityError:
        return jsonify({'error': 'User already exists'}), 409

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, username FROM users WHERE id = %s', (user_id,))
            user = cur.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user[0], 'username': user[1]})

@app.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, password_hash FROM users WHERE username = %s', (username,))
            user = cur.fetchone()
    if not user or not check_password_hash(user[1], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'id': user[0], 'username': username})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)