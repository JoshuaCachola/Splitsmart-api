from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
import os


db = SQLAlchemy()


class User(db.Model):
    """
    Class for Users Table
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    hashed_pw = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255))
    registered_on = db.Column(db.DateTime, nullable=False)

    friend = db.relationship('Friend', back_populates='user')
    expense = db.relationship('Expense', back_populates='user')
    group_users = db.relationship('GroupUsers', backref='users')
    users_friends = db.relationship('UsersFriend', backref='users')
    transaction = db.relationship('Transaction', back_populates='user')
    comment = db.relationship('Comment', back_populates='user')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_pw = generate_password_hash(password, 'sha256')
        self.registered_on = datetime.datetime.now()

    def check_password(self, password):
        return check_password_hash(self.hashed_pw, password)

    def encode_auth_token(self, user_id):
        """
        Generates JWT Token
        """
        try:
            payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(
                days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload,
                              os.environ.get('SECRET_KEY'),
                              algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        """
        try:
            payload = jwt.decode(auth_token,
                                 app.config.get('SECRET_KEY'),
                                 algorithm='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Friend(db.Model):
    """
    Class for Friends table
    """
    __tablename__ = 'friends'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='friend')
    users_friends = db.relationship('UsersFriend', backref='friends')


class UsersFriend(db.Model):
    """
    Class for User and Friends join table
    """
    __tablename__ = 'users_friends'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey(
        'friends.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class Expense(db.Model):
    """
    Class for Expenses Table
    """
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    is_settled = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='expense')
    expense_transactions = db.relationship(
        'ExpenseTransactions', backref='expenses')

    def __init__(self, description, amount, id):
        self.description = description
        self.amount = amount
        self.created_at = datetime.datetime.now()
        self.is_settled = False
        self.user_id = id


class Group(db.Model):
    """
    Class for Groups Table
    """
    __tablename__ = 'groups'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))

    group_users = db.relationship('GroupUsers', backref='groups')


class GroupUsers(db.Model):
    """
    Class for Group Users Join Table
    """
    __tablename__ = 'group_users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(
        'groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Transaction(db.Model):
    """
    Class for Transactions table
    """
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    paid_on = db.Column(db.DateTime)
    is_settled = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='transaction')
    expense_transactions = db.relationship(
        'ExpenseTransactions', backref='transactions')
    comment = db.relationship('Comment', back_populates='transaction')

    def __init__(self, amount, user_id):
        self.amount = amount
        self.user_id = user_id
        self.is_settled = False


class ExpenseTransactions(db.Model):
    """
    Class for Expense Transactions join table
    """
    ___tablename__ = 'expense_transactions'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'))
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))


class Comment(db.Model):
    """
    Class for Comment table
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey(
        'transactions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    transaction = db.relationship('Transaction', back_populates='comment')
    user = db.relationship('User', back_populates='comment')
