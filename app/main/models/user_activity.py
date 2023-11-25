from enum import Enum
from app.extensions import db
from sqlalchemy import text, DateTime


class ActivityType(Enum):
    LOGIN = 'login'
    REQUEST = 'request'


class UserActivity(db.Model):
    __tablename__ = 'user_activity'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_activity', lazy=True))
    path = db.Column(db.String(200), nullable=True)
    request_type = db.Column(db.String(10), nullable=True)
    activity_type = db.Column(db.Enum(ActivityType), nullable=False)
    created_at = db.Column(DateTime, nullable=False, server_default=text('current_timestamp()'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at
        }
