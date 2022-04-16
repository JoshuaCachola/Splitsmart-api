from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import relay

# import models
from src.api.users.model import User as UserModel
from src.api.expense.model import Expense as ExpenseModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class Expense(SQLAlchemyObjectType):
    class Meta:
        model = ExpenseModel
        interfaces = (relay.Node, )
