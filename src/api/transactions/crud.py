from sqlalchemy.exc import SQLAlchemyError

from src import db
from .model import Transaction


def create_transaction(expense_id, user_id, amount):
    return Transaction(expense_id, int(user_id), amount)


def update_transaction(transaction_id, status):
    try:
        transaction = Transaction.query.get(id=transaction_id).first()

        if transaction:
            transaction.payment_status = status
            db.session.commit()
            return transaction
    except SQLAlchemyError as e:
        print(str(e.orig))
        db.session.rollback()
        return None

    return transaction
