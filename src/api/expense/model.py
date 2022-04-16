import datetime
from decimal import Decimal

from src import db


class Expense(db.Model):
    """
    Class for Expenses Table
    """
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(asdecimal=True), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    is_fully_settled = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_at = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='expense')
    transaction = db.relationship('Transaction', back_populates='expense')
    comment = db.relationship('Comment', back_populates='expense')

    def __init__(self, user_id, amount, description):
        self.description = description
        self.amount = amount
        self.is_fully_settled = False
        self.created_at = datetime.datetime.now()
        self.user_id = user_id
        self.updated_at = datetime.datetime.now()

    def __repr__(self):
        return f'<Expense {self.id}>'
    
