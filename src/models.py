import datetime

from flask_sqlalchemy import SQLAlchemy
from src import bcrypt, db


class Friendship(db.Model):
    """
    Class for friendship table between users
        params:
            - status - ['accepted', 'rejected', 'pending']
    """
    __tablename__ = 'friendships'

    id = db.Column(db.Integer, primary_key=True)
    friend1_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    friend2_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime)

    friend1 = db.relationship('User', backref='friendship1',
                              uselist=False, foreign_keys='[Friendship.friend1_id]')
    friend2 = db.relationship('User', backref='friendship2',
                              uselist=False, foreign_keys='[Friendship.friend2_id]')

    def __init__(self, friend1_id, friend2_id):
        self.friend1_id = friend1_id
        self.friend2_id = friend2_id
        self.status = 'pending'
        self.updated_at = datetime.datetime.now()


class Transaction(db.Model):
    """
    Class for Transactions table
    """
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    paid_on = db.Column(db.DateTime)
    is_settled = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey(
        'expenses.id'), nullable=False)
    updated_at = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='transaction')
    expense = db.relationship('Expense', back_populates='transaction')

    def __init__(self, amount, user_id, expense_id):
        self.amount = amount
        self.user_id = user_id
        self.expense_id = expense_id
        self.is_settled = False
        self.updated_at = datetime.datetime.now()


class Comment(db.Model):
    """
    Class for Comment table
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey(
        'expenses.id'), nullable=False)

    user = db.relationship('User', back_populates='comment')
    expense = db.relationship('Expense', back_populates='comment')

    def __init__(self, comment, expense_id, user_id):
        self.comment = comment
        self.expense_id = expense_id
        self.user_id = user_id
        self.date = datetime.datetime.now()
