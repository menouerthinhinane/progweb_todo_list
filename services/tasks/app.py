from flask import Flask, request, jsonify
import psycopg2
import os

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
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    user_id INTEGER NOT NULL
                )
            ''')
init_db()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, title, completed FROM tasks WHERE user_id = %s', (user_id,))
            tasks = [{'id': row[0], 'title': row[1], 'completed': row[2]} for row in cur.fetchall()]
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    user_id = data.get('user_id')
    if not title or not user_id:
        return jsonify({'error': 'title and user_id required'}), 400
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO tasks (title, user_id) VALUES (%s,%s) RETURNING id',
                        (title, user_id))
            task_id = cur.fetchone()[0]
    return jsonify({'id': task_id, 'title': title, 'completed': False}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    completed = data.get('completed')
    if completed is None:
        return jsonify({'error': 'completed field required'}), 400
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('UPDATE tasks SET completed = %s WHERE id = %s RETURNING id', (completed, task_id))
            if not cur.fetchone():
                return jsonify({'error': 'Task not found'}), 404
    return jsonify({'id': task_id, 'completed': completed})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)