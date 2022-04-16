import datetime

from flask import current_app

from src import db, bcrypt 


class User(db.Model):
    """
    Class for Users Table
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    hashed_pw = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255))
    registered_on = db.Column(db.DateTime, nullable=False)
    expense = db.relationship('Expense', back_populates='user')
    transaction = db.relationship('Transaction', back_populates='user')
    comment = db.relationship('Comment', back_populates='user')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_pw = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()
        self.registered_on = datetime.datetime.now()

    def __repr__(self):
        return f'<User {self.email}'

    def to_dict(self):
        return {
            'id': self.id
        }

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_pw, password)

