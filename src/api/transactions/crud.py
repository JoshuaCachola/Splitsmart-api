from .model import Transaction


def create_transaction(expense_id, user_id, amount):
    return Transaction(expense_id, int(user_id), amount)
