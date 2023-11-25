from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory
from flask import abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.main.models.user_activity import UserActivity, ActivityType
from app.main.models.users import User


@jwt_required()
def get_authenticated_user() -> User:
    user_id = get_jwt_identity()

    user = User.get_by_id(user_id)

    if not user:
        abort(401, {"success": False, "error": "Unauthorized"})

    UserActivity(
        user_id=user.id,
        activity_type=ActivityType.REQUEST.value,
        path=request.full_path,
        request_type=request.method
    ).create()

    return user


class RequestContainer(DeclarativeContainer):
    user = Factory(get_authenticated_user)
