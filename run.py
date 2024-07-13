import os
from app import create_app
import eventlet
from app.chat import app as chat_app  # Import the chat app
import threading

flask_app = create_app()

if __name__ == "__main__":
    debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = os.getenv('FLASK_RUN_PORT', 5000)

threading.Thread(target=flask_app.run, kwargs={'debug': debug, 'host': host, 'port': port}).start()
threading.Thread(target=eventlet.wsgi.server, args=(eventlet.listen((host, 8100)), chat_app)).start()