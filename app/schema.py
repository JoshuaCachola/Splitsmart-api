import graphene
from graphene import relay, Connection, Node
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import (
    db, User as UserModel, Expense as ExpenseModel, Friendship as FriendshipModel,
    Transaction as TransactionModel, Comment as CommentModel)
from .util import token_required


# Schema
class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel


class Expense(SQLAlchemyObjectType):
    class Meta:
        model = ExpenseModel


# class Group(SQLAlchemyObjectType):
#     class Meta:
#         model = GroupModel


class Friendship(SQLAlchemyObjectType):
    class Meta:
        model = FriendshipModel


class Transaction(SQLAlchemyObjectType):
    class Meta:
        model = TransactionModel


class Comment(SQLAlchemyObjectType):
    class Meta:
        model = CommentModel


class RecentActivity(graphene.Union):
    class Meta:
        types = (Transaction, Comment, Expense)


# Mutations
class CreateUser(graphene.Mutation):
    """
    Mutation class for users to sign up
    """
    auth_token = graphene.String()
    user = graphene.Field(lambda: User)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, first_name, last_name, email, password):
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


class LoginUser(graphene.Mutation):
    """
    Mutation class to authenticate user and pass frontend JWT token
    """
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
        else:
            return LoginUser(id=None, auth_token=None)


# class CreateGroup(graphene.Mutation):
#     group = graphene.Field(lambda: Group)

#     class Arguments:
#         name = graphene.String(required=True)
#         image = graphene.String()

#     def mutate(self, info, name, image=None):
#         group = GroupModel(
#             name=name,
#             image=image
#         )
#         db.session.add(group)
#         db.session.commit()
#         return CreateGroup(
#             group=group
#         )


class FriendshipRequest(graphene.Mutation):
    """
    Mutation class for users to request other users as friends
    """
    friendship_status = graphene.String()

    class Arguments:
        friend1_id = graphene.Int(required=True)
        friend2_id = graphene.Int(required=True)

    def mutate(self, info, friend1_id, friend2_id):
        # add a check to see if a friend request was already made
        friendship_request = FriendshipModel(
            friend1_id=friend1_id,
            friend2_id=friend2_id
        )
        db.session.add(friendship_request)
        db.session.commit()
        return FriendshipRequest(
            friendship_status=friendship_request.status,
        )


class CreateExpense(graphene.Mutation):
    """
    Mutation class for users to create expenses
    """
    expense = graphene.Field(lambda: Expense)

    class Arguments:
        user_id = graphene.Int(required=True)
        amount = graphene.Float(required=True)
        description = graphene.String(required=True)

    def mutate(self, info, user_id, amount, description):
        expense = ExpenseModel(
            user_id=user_id,
            amount=amount,
            description=description
        )
        db.session.add(expense)
        db.session.commit()
        return CreateExpense(expense=expense)


class CreateTransaction(graphene.Mutation):
    """
    Mutation class for uses to create a transaction from an expense for another
    user to pay
    """
    transaction = graphene.Field(lambda: Transaction)

    class Arguments:
        expense_id = graphene.Int(required=True)
        amount = graphene.Float(required=True)
        user_id = graphene.Int(required=True)

    def mutate(self, info, expense_id, amount, user_id):
        expense_transaction = TransactionModel(
            expense_id=expense_id,
            amount=amount,
            user_id=user_id
        )
        db.session.add(expense_transaction)
        db.session.commit()
        return CreateTransaction(transaction=expense_transaction)


class HandleFriendRequest(graphene.Mutation):
    """
    Mutation class to change the status of a friend request
    """
    change_status = graphene.Boolean()

    class Arguments:
        friend1_id = graphene.Int(required=True)
        friend2_id = graphene.Int(required=True)
        status = graphene.String(required=True)

    def mutate(self, info, friend1_id, friend2_id, status):
        # friends are flipped because how the request is represented in table
        friend_request = FriendshipModel.query.filter_by(friend1_id=friend2_id) \
            .filter_by(friend2_id=friend1_id).first()
        if friend_request:
            friend_request.status = status
            db.session.commit()
            change_status = True
            return HandleFriendRequest(change_status=change_status)
        else:
            change_status = False
            return HandleFriendRequest(change_status=change_status)


class CreateComment(graphene.Mutation):
    """
    Mutation class to create a comment on a transaction
    """
    comment = graphene.Field(lambda: Comment)

    class Arguments:
        comment = graphene.String(required=True)
        expense_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)

    def mutate(self, info, comment, expense_id, user_id):
        create_comment = CommentModel(
            comment=comment,
            expense_id=expense_id,
            user_id=user_id
        )
        db.session.add(create_comment)
        db.session.commit()
        return CreateComment(comment=create_comment)


class Query(graphene.ObjectType):
    # user = graphene.List(User)
    user = graphene.Field(User, email=graphene.String())
    get_friends = graphene.List(Friendship, friend_id=graphene.Int())
    # expense = graphene.Field(Expense, expense_id=graphene.Int())
    active_expenses = graphene.List(Expense, user_id=graphene.Int())
    recent_activity = graphene.List(RecentActivity, user_id=graphene.Int())
    active_transactions = graphene.List(Transaction, user_id=graphene.Int())

    def resolve_user(self, info, email):
        user_query = User.get_query(info)
        return user_query.filter(UserModel.email == email).first()

    def resolve_get_friends(self, info, friend_id):
        friends1_query = Friendship.get_query(info)
        friends2_query = Friendship.get_query(info)
        friend1 = friends1_query.filter(FriendshipModel.friend1_id == friend_id) \
            .filter(FriendshipModel.status == 'accepted')
        friend2 = friends2_query.filter(FriendshipModel.friend2_id == friend_id) \
            .filter(FriendshipModel.status == 'accepted')
        return [*friend1, *friend2]

    # def resolve_expense(self, info, expense_id):
    #     return Expense.query.get(id=expense_id)

    def resolve_active_expenses(self, info, user_id):
        expenses_query = Expense.get_query(info)
        return expenses_query.filter(ExpenseModel.user_id == user_id) \
            .filter(ExpenseModel.is_settled == False)

    def resolve_recent_activity(self, info, user_id):
        transaction_query = Transaction.get_query(info)
        comment_query = Comment.get_query(info)

        transactions = transaction_query.filter(
            TransactionModel.user_id == user_id
        )
        comments = comment_query.filter(CommentModel.user_id == user_id)
        return [*transactions, *comments]

    def resolve_active_transactions(self, info, user_id):
        transaction_query = Transaction.get_query(info)
        return transaction_query.filter(TransactionModel.user_id == user_id)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    create_expense = CreateExpense.Field()
    # create_group = CreateGroup.Field()
    friendship_request = FriendshipRequest.Field()
    create_transaction = CreateTransaction.Field()
    handle_friend_request = HandleFriendRequest.Field()
    create_comment = CreateComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
