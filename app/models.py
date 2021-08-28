
from sqlalchemy import func

from app import db


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

    scope = db.Column(
        db.String(64),
        nullable=False,
        default="user-upload-download-search"
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
