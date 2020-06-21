from app import app
from flask_socketio import SocketIO
import os


socketIo = SocketIO(app, cors_allowed_origins='*')


if __name__ == '__main__':
    socketIo.run(app)
