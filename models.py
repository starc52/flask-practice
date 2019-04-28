from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, unique=True, primary_key=True)
    username = db.Column('username', db.String(255), unique=True, nullable=False)
    password = db.Column('password', db.String, nullable=False)
    loggedIn = db.Column('loggedIn', db.Integer, nullable=False)

    def __repr__(self):
        return f"UserID: {self.id}, Username: {self.username}"
class sacredText(db.Model):
    __tablename__="sacredTexts"

    id = db.Column('id', db.Integer, unique=True, primary_key=True)
    text = db.Column('text', db.String(500), unique=False, nullable=False)
    user = db.Column('user', db.String(255), unique=False, nullable=False)
    def __repr__(self):
        return f"UserId: {self.user}, UserText: {self.text}"
    