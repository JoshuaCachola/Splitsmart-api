from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import relay

# import models
from src.api.users.model import User as UserModel
from src.api.expenses.model import Expense as ExpenseModel
from src.api.transactions.model import Transaction as TransactionModel


class PaymentStatus:
    PENDING = 'pending'
    SETTLED = 'settled'
    CANCELLED = 'cancelled'


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class Expense(SQLAlchemyObjectType):
    class Meta:
        model = ExpenseModel
        interfaces = (relay.Node, )


class Transaction(SQLAlchemyObjectType):
    class Meta:
        model = TransactionModel
        interfaces = (relay.Node, )
