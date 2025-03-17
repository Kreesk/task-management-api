import sqlite3
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, abort
from flask_restful import Api, Resource

load_dotenv()

app = Flask(__name__)
api = Api(app)


ALLOWED_STATUSES = ['todo', 'in_progress', 'done']
DATABASE = os.getenv('DATABASE', 'tasks.db')
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', '5000'))
DEBUG = os.getenv('DEBUG', 'True') == 'True'


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, status TEXT)''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def get_task_or_404(task_id):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = c.fetchone()
        if not task:
            abort(404, description="Task not found")
        return task

class TaskResource(Resource):
    def get(self, task_id=None):
        with get_db_connection() as conn:
            c = conn.cursor()
            if task_id is None:
                c.execute("SELECT * FROM tasks")
                tasks = [{'id' : row[0], 'title' : row[1], 'status' : row[2]} for row in c.fetchall()]
                return jsonify(tasks)
            else:
                task = get_task_or_404(task_id)
                return jsonify({'id' : task[0], 'title' : task[1], 'status' : task[2]})

    def post(self):
        data = request.get_json()
        if not data or 'title' not in data or not data['title'].strip():
            return {'error' : 'Title is required and cannot be empty'}, 400
        if len(data['title']) > 100:
            return {'error' : 'Title must be less than 100 characters'}, 400
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", (data['title'], 'todo'))
            conn.commit()
            task_id = c.lastrowid
            return {'id' : task_id, 'title' : data['title'], 'status' : 'todo'}, 201

    def put(self, task_id):
        task = get_task_or_404(task_id)
        data = request.get_json()
        if not data or 'status' not in data:
            return {'error' : 'Status is required'}, 400
        if data['status'] not in ALLOWED_STATUSES:
            return {'error' : f'Status must be one of {ALLOWED_STATUSES}'}, 400
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("UPDATE tasks SET status = ? WHERE id = ?", (data['status'], task_id))
            conn.commit()
        return {'message' : f'Task {task_id} updated', 'status' : data['status']}, 200

    def delete(self, task_id):
        task = get_task_or_404(task_id)
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
        return  {'message' : f'Task {task_id} deleted'}, 200

api.add_resource(TaskResource, '/api/tasks', '/api/tasks/<int:task_id>')

@app.route('/')
def index():
    return "Task Management API - Use /tasks to see tasks or /api/tasks for REST API"

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    with get_db_connection() as conn:
        c = conn.cursor()
        if request.method == 'POST':
            title = request.form.get('title')
            if not title or not title.strip():
                return "Title is required", 400
            if len(title) > 100:
                return "Title must be less than 100 characters", 400
            c.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", (title, 'todo'))
            conn.commit()

        c.execute('SELECT * FROM tasks')
        tasks_list = [{'id' : row[0], 'title' : row[1], 'status' : row[2]} for row in c.fetchall()]
    return render_template('tasks.html', tasks=tasks_list)

if __name__ == '__main__':
    init_db()
    app.run(debug=DEBUG, host=HOST, port=PORT)