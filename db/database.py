from flask_login import UserMixin
from . import db


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, email, password_hash, name):
        self.email = email
        self.password_hash = password_hash
        self.name = name
