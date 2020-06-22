import graphene
from graphene import relay, Connection, Node
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet
from .models import (
    db, User as UserModel, Expense as ExpenseModel, Group as GroupModel,
    UsersFriend as UsersFriendModel, Friend as FriendModel)


# Schema
class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


# class UserFilter(FilterSet):
#     class Meta:
#         fields: {
#             'email': ['eq']
#         }


# class UserFilterableConnectionField(FilterableConnectionField):
#     filters = {UserModel: UserFilter()}


# class UserNode(SQLAlchemyObjectType):
#     class Meta:
#         model = UserModel
#         connection_field_factory = UserFilterableConnectionField.factory


# class UserConnection(Connection):
#     class Meta:
#         node = UserNode


class Expense(SQLAlchemyObjectType):
    class Meta:
        model = ExpenseModel
        interfaces = (relay.Node, )


class Group(SQLAlchemyObjectType):
    class Meta:
        model = GroupModel
        interfaces = (relay.Node, )


class UsersFriend(SQLAlchemyObjectType):
    class Meta:
        model = UsersFriendModel
        interfaces = (relay.Node, )


class Friend(SQLAlchemyObjectType):
    class Meta:
        model = FriendModel
        interfaces = (relay.Node, )


# Mutations
class CreateUser(graphene.Mutation):
    auth_token = graphene.String()
    user = graphene.Field(lambda: User)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(
            self, info, first_name, last_name, email, password):
        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        return CreateUser(
            user=user,
            auth_token=auth_token
        )


class CreateExpense(graphene.Mutation):
    expense = graphene.Field(lambda: Expense)

    class Arguments:
        description = graphene.String(required=True)
        amount = graphene.Float(required=True)

    def mutate(self, info, description, amount):
        expense = ExpenseModel(description=description, amount=amount)
        db.session.add(expense)
        db.session.commit()

        return CreateExpense(
            expense=expense
        )


class LoginUser(graphene.Mutation):
    id = graphene.Int()
    auth_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = UserModel.query.filter_by(email=email).first()
        if user and user.check_password(password):
            auth_token = user.encode_auth_token(user.id)
        return LoginUser(
            id=user.id,
            auth_token=auth_token
        )


class CreateGroup(graphene.Mutation):
    group = graphene.Field(lambda: Group)

    class Arguments:
        name = graphene.String(required=True)
        image = graphene.String()

    def mutate(self, info, name, image=None):
        group = GroupModel(
            name=name,
            image=image
        )
        db.session.add(group)
        db.session.commit()
        return CreateGroup(
            group=group
        )


class AddFriend(graphene.Mutation):
    users_friend = graphene.Field(lambda: UsersFriend)
    friend = graphene.Field(lambda: Friend)

    class Arguments:
        user_id = graphene.Int(required=True)
        friend_id = graphene.Int(required=True)

    def mutate(self, info, user_id, friend_id):
        friend = FriendModel(user_id=friend_id)
        db.session.add(friend)
        db.session.commit()

        users_friend = UsersFriendModel(
            user_id=user_id,
            friend_id=friend.id
        )
        db.session.add(users_friend)
        db.session.commit()

        return AddFriend(users_friend=users_friend, friend=friend)


class GetUser(graphene.ObjectType):
    first_name = graphene.String()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # user = graphene.List(User)
    user = graphene.Field(User, email=graphene.String())
    # expense = graphene.Field(Expense, expense_id=graphene.Int())
    # expenses = graphene.Field(Expense, user_id=graphene.Int())

    def resolve_user(self, info, email):
        user = User.get_query(info)
        return user.filter(UserModel.email == email).first()

    # def resolve_expense(self, info, expense_id):
    #     return Expense.query.get(id=expense_id)

    # def resolve_expenses(self, info, user_id):
    #     return Expense.query.filter_by(user_id=user_id).all()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    create_expense = CreateExpense.Field()
    create_group = CreateGroup.Field()
    add_friend = AddFriend.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
