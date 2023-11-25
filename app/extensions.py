from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
jwt = JWTManager()
bcrypt = Bcrypt()
