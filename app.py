from app import create_app
from app.extensions import socketio

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
