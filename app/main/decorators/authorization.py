from functools import wraps
from flask import request
from app.main.utils.auth import get_bearer_token
from config import Config


def internal_authorized(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = get_bearer_token(request)

        if token != Config.JWT_PROJECT_KEY:
            return {"success": False, "error": "Unauthorized"}, 401

        return fn(*args, **kwargs)

    return wrapper
