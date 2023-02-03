from datetime import datetime

from flask import url_for
import sqlalchemy as sq

from application import db


class Blog(db.Model):
    __tablename__ = 'blog'

    id = sq.Column(sq.Integer, primary_key=True)
    slug = sq.Column(sq.String, unique=True, nullable=False)
    title = sq.Column(sq.String, nullable=False)
    content = sq.Column(sq.String, nullable=False)
    date = sq.Column(sq.DateTime, default=datetime.utcnow)

    author_id = sq.Column(sq.Integer, sq.ForeignKey('user.id'))

    def get_absolute_url(self):
        return url_for('blog.detail', slug=self.slug)

    def __repr__(self):
        return f"<Blog {self.title}>"
