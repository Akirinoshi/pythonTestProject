import flask_pydantic
from flask import Flask
from flask_cors import CORS

from app.patches.route_validation import validate_path_params
from app.extensions import db, socketio, migrate, jwt
from app.loger import init_logging
from config import Config

global_socketio = None


def create_app(config_class=Config):
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    CORS(app, resources={r"/*": {"origins": "*"}})

    apply_monkey_patches()

    register_extensions(app)

    create_di_containers(app)
    register_blueprints(app)

    return app


def create_di_containers(app: Flask) -> None:
    from app.common.containers import RequestContainer

    request_container = RequestContainer()

    request_container.wire(
        packages=[
            "app.main.routes",
        ]
    )

    app.request_container = request_container


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    init_logging(app)
    migrate.init_app(app, db)
    global global_socketio
    if global_socketio is None:
        socketio.init_app(app, cors_allowed_origins="*")
        global_socketio = socketio

    jwt.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    from app.main import main_bp
    app.register_blueprint(main_bp)
    from app.main.routes.users import user_bp
    app.register_blueprint(user_bp)
    from app.main.routes.posts import post_bp
    app.register_blueprint(post_bp)
    from app.main.routes.analytics import analytics_bp
    app.register_blueprint(analytics_bp)


def apply_monkey_patches():
    flask_pydantic.core.validate_path_params = validate_path_params

