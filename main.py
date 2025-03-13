import uvicorn

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
api = Api(app)

tasks_list = []

class TaskResource(Resource):
    def get(self):
        return jsonify(tasks_list)

    def post(self):
        data = request.get_json()
        if not data or 'title' not in data:
            return {'error' : 'Title is required'}, 400
        new_task = {
            'id' : len(tasks_list) +1,
            "title" : data['title'],
            'status' : 'todo'
        }
        tasks_list.append(new_task)
        return new_task, 201

api.add_resource(TaskResource, '/api/tasks')

@app.route('/')
def index():
    return "Task Management API - Use /tasks to see tasks or /api/tasks for REST API"

@app.route('/tasks', methods=['GET'])
def tasks():
    return render_template('tasks.html', tasks=tasks_list)

if __name__ == '__main__':
    uvicorn.run(asgi_app, host='127.0.0.1', port=5000)