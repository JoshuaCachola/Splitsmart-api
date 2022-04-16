from sqlalchemy.exc import SQLAlchemyError

from src import db
from .model import Expense


def create_expense(user_id, amount, description):
    try:
        expense = Expense(user_id, amount, description)
        db.session.add(expense)
        db.session.commit() 
    except SQLAlchemyError as e:
        error = str(e.orig)
        return error

    return expense
