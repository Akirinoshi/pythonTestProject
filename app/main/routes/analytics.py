# Import required libraries and modules
from flask import Blueprint
from flask_pydantic import validate
from app.main.decorators.authorization import internal_authorized
from app.main.models.post_likes import PostLikes
from app.main.models.user_activity import UserActivity, ActivityType
from app.main.models.users import User
from app.main.schemas.analytics import AnalyticsLikeQuery
from flask import jsonify
from sqlalchemy import func, case
from app.extensions import db

from datetime import timedelta

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics/")


@analytics_bp.route('/likes/', methods=['GET'])
@validate()
@internal_authorized
def like_analytics(query: AnalyticsLikeQuery):
    date_from = query.date_from
    date_to = query.date_to

    # Query like and dislike counts within the specified date range
    likes_data = (
        PostLikes.query
        .with_entities(func.date(PostLikes.created_at).label('date'),
                       func.sum(case((PostLikes.like, 1), else_=0)).label('like_count'),
                       func.sum(case((PostLikes.like.is_(False), 1), else_=0)).label('dislike_count'))
        .filter(PostLikes.created_at.between(date_from, date_to))
        .group_by(func.date(PostLikes.created_at))
        .all()
    )

    # Process data into a dictionary with date as keys and like/dislike counts as values
    analytics_result = {str(date): {'like_count': like_count, 'dislike_count': dislike_count}
                        for date, like_count, dislike_count in likes_data}

    return jsonify(analytics_result)


@analytics_bp.route('/user/last_activity/<int:user_id>', methods=['GET'])
@validate()
@internal_authorized
def user_last_activity(user_id):
    # Check if the user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Get the last login and last request activities of the user
    last_activity_times = (
        UserActivity.query
        .filter_by(user_id=user_id)
        .group_by(UserActivity.user_id)
        .with_entities(
            UserActivity.user_id,
            func.max(case((UserActivity.activity_type == 'login', UserActivity.created_at)))
            .label('last_login_time'),
            func.max(case((UserActivity.activity_type == 'request', UserActivity.created_at)))
            .label('last_request_time')
        )
        .first()
    )

    if not last_activity_times:
        return 'Not found', 404

    response = {
        "last_login_time": last_activity_times.last_login_time,
        "last_request_time": last_activity_times.last_request_time
    }

    return response, 200
