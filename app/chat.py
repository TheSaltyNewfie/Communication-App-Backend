import eventlet
import socketio
import os
from .utils.database import Database
import json
import datetime
import redis

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    #nothing yet


@sio.event
def message(sid, data):
    print('message ', data)
    sio.emit('newMessage', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    print('Starting server...')
    eventlet.wsgi.server(eventlet.listen(
        (os.getenv('FLASK_RUN_HOST', '127.0.0.1'), 8100)), app)
