import sqlite3

from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, status TEXT)''')
    conn.commit()
    conn.close()

class TaskResource(Resource):
    def get(self, task_id=None):
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        if task_id is None:
            c.execute("SELECT * FROM tasks")
            tasks = [{'id' : row[0], 'title' : row[1], 'status' : row[2]} for row in c.fetchall()]
            conn.close()
            return jsonify(tasks)
        else:
            c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            task = c.fetchone()
            conn.close()

            if task:
                return jsonify({'id' : task[0], 'title' : task[1], 'status' : task[2]})

            return {'error' : 'Task not found'}, 404

    def post(self):
        data = request.get_json()
        if not data or 'title' not in data:
            return {'error' : 'Title is required'}, 400
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", (data['title'], 'todo'))
        conn.commit()
        task_id = c.lastrowid
        conn.close()
        return {'id' : task_id, 'title' : data['title'], 'status' : 'todo'}, 201

    def put(self, task_id):
        data = request.get_json()
        if not data or 'status' not in data:
            return {'error' : 'Status is required'}, 400

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = c.fetchone()

        if not task:
            conn.close()
            return {'error' : 'Task not found'}, 404

        c.execute("UPDATE tasks SET status = ? WHERE id = ?", (data['status'], task_id))
        conn.commit()
        conn.close()

        return {'message' : f'Task {task_id} updated', 'status' : data['status']}, 200

    def delete(self, task_id):
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = c.fetchone()

        if not task:
            conn.close()
            return {'error' : 'Task not found'}, 404

        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return {'message' : f'Task {task_id} deleted'}, 200

api.add_resource(TaskResource, '/api/tasks', '/api/tasks/<int:task_id>')

@app.route('/')
def index():
    return "Task Management API - Use /tasks to see tasks or /api/tasks for REST API"

@app.route('/tasks', methods=['GET'])
def tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks_list = [{'id' : row[0], 'title' : row[1], 'status' : row[2]} for row in c.fetchall()]
    conn.close()
    return render_template('tasks.html', tasks=tasks_list)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)