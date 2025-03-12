import asyncio
import uvicorn

from asgiref.wsgi import WsgiToAsgi
from flask import Flask

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

@app.route('/')
def index():
    return "Task Management API"

if __name__ == '__main__':
    uvicorn.run(asgi_app, host='127.0.0.1', port=5000)