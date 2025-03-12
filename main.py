import asyncio
import uvicorn

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, render_template, request
from flask_restful import Api, Resource

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
api = Api(app)

tasks = []

class TaskResource(Resource):
    def get(self):
        return {'task': tasks}

    def post(self):
        data = request.get_json()
        new_task = {'id' : len(tasks) + 1, 'title' : data['title'], 'status' : 'todo'}
        tasks.append(new_task)
        return new_task, 201

api.add_resource(TaskResource, '/tasks')

@app.route('/')
def index():
    return "Task Management API"

if __name__ == '__main__':
    uvicorn.run(asgi_app, host='127.0.0.1', port=5000)