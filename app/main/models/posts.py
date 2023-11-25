from enum import Enum
from typing import Optional

from app.extensions import db
from sqlalchemy import text, DateTime
from app.extensions import bcrypt


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_post', lazy=True))
    created_at = db.Column(DateTime, nullable=False, server_default=text('current_timestamp()'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True

    def update(self):
        db.session.commit()
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at
        }
