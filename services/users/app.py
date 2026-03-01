from flask import Flask, request, jsonify
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ma-cle-secrete-tres-simple-pour-dev'

def get_db():
    """Connexion à PostgreSQL"""
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', '5432'),
        database=os.environ.get('DB_NAME', 'usersdb'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        cursor_factory=RealDictCursor
    )

def init_db():
    """Crée la table users si elle n'existe pas"""
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(80) UNIQUE NOT NULL,
                        email VARCHAR(120) UNIQUE NOT NULL,
                        password_hash VARCHAR(200) NOT NULL
                    )
                ''')
                conn.commit()
        print("✅ Table 'users' prête")
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")

init_db()

@app.route('/users', methods=['POST'])
def create_user():
    """Inscription"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Champs requis: username, email, password'}), 400
    
    password_hash = generate_password_hash(password)
    
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id',
                    (username, email, password_hash)
                )
                user_id = cur.fetchone()['id']
                conn.commit()
        
        return jsonify({
            'id': user_id,
            'username': username,
            'email': email
        }), 201
        
    except psycopg2.errors.UniqueViolation:
        return jsonify({'error': 'Nom d\'utilisateur ou email déjà utilisé'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/login', methods=['POST'])
def login():
    """Connexion"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username et password requis'}), 400
    
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT id, username, email, password_hash FROM users WHERE username = %s',
                    (username,)
                )
                user = cur.fetchone()
        
        if not user or not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Identifiants incorrects'}), 401
        
        # Génère un token simple
        token = jwt.encode({
            'user_id': user['id'],
            'username': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Récupère un utilisateur"""
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT id, username, email FROM users WHERE id = %s',
                    (user_id,)
                )
                user = cur.fetchone()
        
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        return jsonify(user), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)