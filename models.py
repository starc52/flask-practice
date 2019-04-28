from flask_sqlalchemy import SQLAlchemy

from password_mgm import *

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, unique=True, primary_key=True)
    username = db.Column('username', db.String(255), unique=True, nullable=False)
    password = db.Column('password', db.String, nullable=False)

    def __repr__(self):
        return f"UserID: {self.id}, Username: {self.username}"

    