from datetime import timedelta
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from flask_pydantic import validate
from flask import Blueprint
from app.main.decorators.authorization import internal_authorized
from app.main.models.user_activity import ActivityType, UserActivity
from app.main.models.users import User
from app.main.schemas.users import UsersSignUpModel, UsersSignInModel

user_bp = Blueprint("user", __name__, url_prefix="/api/user/")


@user_bp.route('/signup', methods=['POST'])
@validate()
@internal_authorized
def create_user(body: UsersSignUpModel):
    email = body.email
    password = body.password

    if User.get_by_email(email):
        return 'User with such email already exists', 401

    User(email, password).create()

    return 'Success', 200


@user_bp.route('/signin', methods=['POST'])
@validate()
@internal_authorized
def signin(body: UsersSignInModel):
    email = body.email
    password = body.password

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        UserActivity(
            user_id=user.id,
            activity_type=ActivityType.LOGIN.value,
            path=request.full_path,
            request_type=request.method
        ).create()

        # Generate a JWT token with a one-month expiration time
        expires = timedelta(days=30)
        access_token = create_access_token(identity=user.id, expires_delta=expires)
        return jsonify(access_token=access_token)

    return 'Invalid email or password', 401
