from sqlalchemy.exc import SQLAlchemyError

from src import db
from .model import Expense
from ..transactions.crud import create_transaction


def create_expense(user_id, total, description, transactions):
    try:
        expense = Expense(user_id, total, description)
        db.session.add(expense)
        db.session.commit()
        for user_id, amount in transactions.items():
            transaction = create_transaction(expense.id, user_id, amount)
            db.session.add(transaction)
            db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.orig)
        db.rollback()
        return error

    return expense
