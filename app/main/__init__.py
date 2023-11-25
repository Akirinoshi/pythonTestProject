from flask import Blueprint

main_bp = Blueprint("main", __name__, url_prefix="/api/")

from app.main.routes import (
    users,
    posts
)

from app.main.models import (
    users,
    posts,
    post_likes,
    user_activity
)
