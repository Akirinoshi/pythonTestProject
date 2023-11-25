from enum import Enum
from typing import Optional

from app.extensions import db
from sqlalchemy import text, DateTime
from app.extensions import bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(DateTime, nullable=False, server_default=text('current_timestamp()'))

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        return cls.query.filter_by(id=user_id).first()

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self.id
