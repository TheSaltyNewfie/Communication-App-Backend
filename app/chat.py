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

users = {
    "0": [
        ["admin", "0", 00000000]  # [username, user_id, last_heartbeat]
    ],
}


@sio.event
def heartbeat(sid, data):
    # Heartbeat will take data from the user, store it in memory, and then emit it to all other users
    print('heartbeat ', sid)

    # data should look like {"username": "example", "conversation": "1", "user_id": "1"}
    parsed = json.loads(data)

    Database("app/data.db").execute("update Users set is_online = ? where username = ?",
                                    True, parsed['username'])

    print(parsed)

    for conversation in users:  # temp solution to have accurate data
        users.pop(conversation)

    currentTime = datetime.datetime.now()
    users[parsed['conversation']].append(
        [parsed['username'], parsed['user_id'], currentTime])

    print(users)

    sio.emit('update', users)


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    Database().set_cache(sid, "connected")


@sio.event
def message(sid, data):
    print('message ', data)
    sio.emit('newMessage', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


def send_heartbeat():
    while True:
        print('sending heartbeat request')
        sio.emit('heartbeatRequest')
        eventlet.sleep(30)


eventlet.spawn(send_heartbeat)

if __name__ == '__main__':
    eventlet.monkey_patch()  # Ensure all standard library modules are patched
    eventlet.spawn(send_heartbeat)
    print('Starting server...')
    eventlet.wsgi.server(eventlet.listen(
        (os.getenv('FLASK_RUN_HOST', '127.0.0.1'), 8100)), app)
