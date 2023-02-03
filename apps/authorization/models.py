from datetime import datetime

from flask_login import UserMixin
import sqlalchemy as sq

from application import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    username = sq.Column(sq.String, unique=True, nullable=False)

    email = sq.Column(sq.String, nullable=False)
    is_active = sq.Column(sq.Boolean, default=False)

    psw_hash = sq.Column(sq.String(500), nullable=False)

    join_date = sq.Column(sq.DateTime, default=datetime.utcnow)
    last_login = sq.Column(sq.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.id}>"
