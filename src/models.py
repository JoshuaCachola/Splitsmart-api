
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


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
        self.hashed_pw = generate_password_hash(password, 'sha256')
        self.registered_on = datetime.datetime.now()

    def to_dict(self):
        return {
            'id': self.id
        }

    def check_password(self, password):
        return check_password_hash(self.hashed_pw, password)


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


class Expense(db.Model):
    """
    Class for Expenses Table
    """
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    is_settled = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_at = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='expense')
    transaction = db.relationship('Transaction', back_populates='expense')
    comment = db.relationship('Comment', back_populates='expense')

    def __init__(self, description, amount, user_id):
        self.description = description
        self.amount = amount
        self.created_at = datetime.datetime.now()
        self.is_settled = False
        self.user_id = user_id
        self.updated_at = datetime.datetime.now()


# class Group(db.Model):
#     """
#     Class for Groups Table
#     """
#     __tablename__ = 'groups'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     image = db.Column(db.String(255))

#     group_users = db.relationship('GroupUsers', backref='groups')


# class GroupUsers(db.Model):
#     """
#     Class for Group Users Join Table
#     """
#     __tablename__ = 'group_users'

#     id = db.Column(db.Integer, primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey(
#         'groups.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


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
