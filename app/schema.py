import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db, User as UserModel, Expense as ExpenseModel


# Users
class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class CreateUser(graphene.Mutation):
    id = graphene.Int()
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    avatar = graphene.String()
    password = graphene.String(required=True)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        avatar = graphene.String()
        password = graphene.String(required=True)

    def mutate(
            self, info, first_name, last_name, email, avatar, password):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            avatar=avatar,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        return {
            'status': 'success',
            'message': 'Successfully registered.',
            'auth_token': auth_token.decode()
        }


# Expenses
class Expense(SQLAlchemyObjectType):
    class Meta:
        model = ExpenseModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(User.connection)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
