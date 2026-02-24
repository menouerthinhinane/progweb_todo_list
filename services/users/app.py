from flask import Flask, request, jsonify
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db():
    """Connexion à PostgreSQL avec paramètres depuis variables d'environnement"""
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
                        password_hash VARCHAR(200) NOT NULL, 
                        email VARCHAR(120) UNIQUE NOT NULL     
                    )
                ''')
                conn.commit()
        print(" Table 'users' prête")
    except Exception as e:
        print(f" Erreur d'initialisation: {e}")

# Initialiser la base au démarrage
init_db()

@app.route('/users', methods=['POST'])
def create_user():
    """Inscription d'un nouvel utilisateur"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not username or not password or not email:
        return jsonify({'error': 'Username, password et email requis'}), 400
    
    password_hash = generate_password_hash(password)
    
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id',
                    (username, password_hash)
                )
                user_id = cur.fetchone()['id']
                conn.commit()
        return jsonify({'id': user_id, 'username': username}), 201
    except psycopg2.IntegrityError:
        return jsonify({'error': 'Nom d\'utilisateur deja existant'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/login', methods=['POST'])
def login():
    """Authentification d'un utilisateur"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT id, password_hash FROM users WHERE username = %s',
                    (username,)
                )
                user = cur.fetchone()
        
        if not user or not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Identifiants incorrects'}), 401
        
        return jsonify({'id': user['id'], 'username': username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Récupère un utilisateur par son ID"""
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT id, username FROM users WHERE id = %s',
                    (user_id,)
                )
                user = cur.fetchone()
        
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)