from flask import Flask, request, jsonify
import psycopg2
import os
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', '5432'),
        database=os.environ.get('DB_NAME', 'tasksdb'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        cursor_factory=RealDictCursor
    )

def init_db():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        description TEXT,
                        completed BOOLEAN DEFAULT FALSE,
                        user_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        print("✅ Table 'tasks' prête")
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")

init_db()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id requis'}), 400
    
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT id, title, description, completed, created_at FROM tasks WHERE user_id = %s ORDER BY created_at DESC',
                    (user_id,)
                )
                tasks = cur.fetchall()
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    user_id = data.get('user_id')
    
    if not title or not user_id:
        return jsonify({'error': 'title et user_id requis'}), 400
    
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO tasks (title, description, user_id) VALUES (%s, %s, %s) RETURNING id, created_at',
                    (title, description, user_id)
                )
                task = cur.fetchone()
                conn.commit()
        
        return jsonify({
            'id': task['id'],
            'title': title,
            'description': description,
            'completed': False,
            'user_id': user_id,
            'created_at': task['created_at']
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    completed = data.get('completed')
    
    if completed is None:
        return jsonify({'error': 'completed requis'}), 400
    
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'UPDATE tasks SET completed = %s WHERE id = %s RETURNING id',
                    (completed, task_id)
                )
                updated = cur.fetchone()
                conn.commit()
        
        if not updated:
            return jsonify({'error': 'Tâche non trouvée'}), 404
        
        return jsonify({'id': task_id, 'completed': completed}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'DELETE FROM tasks WHERE id = %s RETURNING id',
                    (task_id,)
                )
                deleted = cur.fetchone()
                conn.commit()
        
        if not deleted:
            return jsonify({'error': 'Tâche non trouvée'}), 404
        
        return jsonify({'message': 'Tâche supprimée'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)