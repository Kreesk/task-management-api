import sqlite3
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, abort, make_response, session, redirect
from flask_restful import Api, Resource
from contextlib import contextmanager

app = Flask(__name__)
app.secret_key = 'FLASK_APP_KEY'
api = Api(app)
load_dotenv(override=True)

ALLOWED_STATUSES = ['todo', 'in_progress', 'done']
USERNAME = os.getenv('USERNAME', 'admin')
PASSWORD = os.getenv('PASSWORD', 'password')
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

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()

def get_all_tasks():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM tasks')
        return [{'id': row[0], 'title': row[1], 'status': row[2]} for row in c.fetchall()]

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
        get_task_or_404(task_id)
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
        get_task_or_404(task_id)
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
    if 'logged_in' not in session or not session['logged_in']:
        return redirect('/login')
    if request.method == 'POST':
        title = request.form.get('title')
        if not title or not title.strip():
            return "Title is required", 400
        if len(title) > 100:
            return "Title must be less than 100 characters", 400
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", (title, 'todo'))
            conn.commit()
    tasks_list = get_all_tasks()
    return render_template('tasks.html', tasks=tasks_list)

@app.route('/tasks/<int:task_id>/done', methods=['POST'])
def mark_task_done(task_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect('/login')
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = c.fetchone()
        if not task:
            return "Задача не найдена!", 404
        c.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
        conn.commit()
    tasks_list = get_all_tasks()
    return  render_template('tasks.html', tasks=tasks_list)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect('/tasks')
        else:
            return render_template('login.html', error='Неверный логин или пароль')
    return render_template('login.html')

def check_auth():
    auth = request.authorization
    if not auth or auth.username != USERNAME or auth.password != PASSWORD:
        return make_response("Login required!", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return True

if __name__ == '__main__':
    init_db()
    app.run(debug=DEBUG, host=HOST, port=PORT)