
from sqlalchemy import func

from app import db


class Login(db.Model):
    idx = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    user_agent = db.Column(
        db.String(500),
        nullable=False
    )

    token = db.Column(
        db.String(128),
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    expired = db.Column(
        db.DateTime,
        nullable=False,
    )

    def __repr__(self):
        return f"<Login idx={self.idx}, user_id={self.user_id}>"


class User(db.Model):
    idx = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    email = db.Column(
        db.String(128),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(128),
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    def __repr__(self):
        return f"<User idx={self.idx}, email={self.email!r}>"


class File(db.Model):
    uuid = db.Column(
        db.String(36),
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner = db.Column(
        db.Integer,
        nullable=False
    )

    name = db.Column(
        db.String(256),
        nullable=False,
        default="untitled file"
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    def __repr__(self):
        return f"<File uuid={self.uuid!r}>"


class Key(db.Model):
    uuid = db.Column(
        db.String(36),
        unique=True,
        primary_key=True,
        nullable=False
    )

    key = db.Column(
        db.String(64),
        nullable=False,
    )

    iv = db.Column(
        db.String(32),
        nullable=False,
    )

    def __repr__(self):
        return f"<Key uuid={self.uuid!r}>"
