import datetime

from enum import Enum
from decimal import Decimal

from src import db


class PaymentStatus(Enum):
    PENDING = 'pending'
    SETTLED = 'settled'
    CANCELLED = 'cancelled'
    FAILED = 'failed'
    EXPIRED = 'expired'


class Transaction(db.Model):
    """
    Class for Transactions table
    """
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(), nullable=False)
    paid_on = db.Column(db.DateTime)
    payment_status = db.Column(db.Enum(PaymentStatus))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey(
        'expenses.id'), nullable=False)
    updated_at = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='transaction')
    expense = db.relationship('Expense', back_populates='transaction')

    def __init__(self, expense_id, user_id, amount):
        self.amount = Decimal(amount)
        self.user_id = user_id
        self.expense_id = expense_id
        self.payment_status = PaymentStatus.PENDING
        self.update_at = datetime.datetime.now()

    def __repr__(self):
        return f'<Transaction {self.id}>'
