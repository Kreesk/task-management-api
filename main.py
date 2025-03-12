import asyncio
import uvicorn

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, render_template, request
from flask_restful import Api, Resource

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
api = Api(app)

tasks_list = []

@app.route('/')
def index():
    return "Task Management API"

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        data = request.form
        new_task = {'id' : len(tasks_list) + 1, 'title' : data['title'], 'status' : 'todo'}
        tasks_list.append(new_task)
    return render_template('tasks.html', tasks=tasks_list)

if __name__ == '__main__':
    uvicorn.run(asgi_app, host='127.0.0.1', port=5000)