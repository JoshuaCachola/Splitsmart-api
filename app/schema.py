import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import (
    db, User as UserModel, Expense as ExpenseModel, Friendship as FriendshipModel,
    Transaction as TransactionModel, Comment as CommentModel)
from flask_jwt_extended import create_access_token, jwt_required
import datetime


# Schema
class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        # interfaces = (relay.Node, )


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
        types = (Transaction, Friendship)


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
        """
        :type first_name: string
        :type last_name: string
        :type email: string
        :type password: string
        :rtype: object
        """
        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        auth_token = create_access_token(user.id)
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
    # refresh_token = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    # @classmethod
    # @login.user_loader
    def mutate(self, info, email, password):
        """
        :type email: string
        :type password: string
        :rtype: object
        """
        user = UserModel.query.filter_by(email=email).first()
        if user:
            auth_token = create_access_token(user.id)
            return LoginUser(
                id=user.id,
                auth_token=auth_token,
                first_name=user.first_name,
                last_name=user.last_name,
                # refresh_token=refresh_token
            )
        else:
            return LoginUser(
                id=None,
                auth_token=None,
                first_name=None,
                last_name=None,
                # refresh_token=None
            )


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

    @jwt_required
    def mutate(self, info, friend1_id, friend2_id):
        """
        :type friend1_id: int
        :type friend1_id: int
        :rtype: obj
        """
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

    @jwt_required
    def mutate(self, info, user_id, amount, description):
        """
        :type user_id: int
        :type amount: float
        :type description: string
        :rtype: obj
        """
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

    @jwt_required
    def mutate(self, info, expense_id, amount, user_id):
        """
        :type expense_id: int
        :type amount: float
        :type user_id: int
        :rtype: obj
        """
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
    friend_request = graphene.Field(lambda: Friendship)

    class Arguments:
        id = graphene.Int(required=True)
        status = graphene.String(required=True)

    @jwt_required
    def mutate(self, info, id, status):
        """
        :type id: int
        :type status: string
        :rtype: obj
        """
        friend_request = FriendshipModel.query.filter_by(id=id).first()
        friend_request.status = status
        friend_request.updated_at = datetime.datetime.now()
        db.session.commit()
        return HandleFriendRequest(friend_request=friend_request)


class CreateComment(graphene.Mutation):
    """
    Mutation class to create a comment on a transaction
    """
    comment = graphene.Field(lambda: Comment)

    class Arguments:
        comment = graphene.String(required=True)
        expense_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)

    @jwt_required
    def mutate(self, info, comment, expense_id, user_id):
        """
        :type comment: string
        :type expense_id: int
        :type user_id: int
        :rtype: obj
        """
        create_comment = CommentModel(
            comment=comment,
            expense_id=expense_id,
            user_id=user_id
        )
        db.session.add(create_comment)
        db.session.commit()
        return CreateComment(comment=create_comment)


class HandleTransaction(graphene.Mutation):
    """
    Mutation class to handle paying a transaction
    """
    transaction = graphene.Field(lambda: Transaction)

    class Arguments:
        id = graphene.Int(required=True)

    @jwt_required
    def mutate(self, info, id):
        """
        :type id: int
        :rtype: obj
        """
        transaction = TransactionModel.query.filter_by(id=id).first()
        transaction.paid_on = datetime.datetime.now()
        transaction.updated_at = datetime.datetime.now()
        transaction.is_settled = True
        db.session.commit()
        return HandleTransaction(transaction=transaction)


class Query(graphene.ObjectType):
    user = graphene.Field(User, email=graphene.String())
    get_friends = graphene.List(
        Friendship, friend_id=graphene.Int())
    active_expenses = graphene.List(Expense, user_id=graphene.Int())
    recent_activity = graphene.List(RecentActivity, user_id=graphene.Int())
    active_transactions = graphene.List(Transaction, user_id=graphene.Int())
    get_expense_comments = graphene.List(
        Comment, expense_id=graphene.Int())
    get_expense_transactions = graphene.List(
        Transaction, expense_id=graphene.Int())
    get_all_users = graphene.List(User)

    def resolve_user(self, info, email):
        user_query = User.get_query(info)
        user = user_query.filter(UserModel.email == email).first()
        if user:
            return user
        else:
            return None

    @jwt_required
    def resolve_get_friends(self, info, friend_id):
        friends1_query = Friendship.get_query(info)
        friends2_query = Friendship.get_query(info)
        friend1 = friends1_query.filter(FriendshipModel.friend1_id == friend_id) \
            .filter(FriendshipModel.status == 'accepted')
        friend2 = friends2_query.filter(FriendshipModel.friend2_id == friend_id) \
            .filter(FriendshipModel.status == 'accepted')

        return [*friend1, *friend2]

    @jwt_required
    def resolve_active_expenses(self, info, user_id):
        expenses_query = Expense.get_query(info)
        return expenses_query.filter(ExpenseModel.user_id == user_id) \
            .filter(ExpenseModel.is_settled == False)

    @jwt_required
    def resolve_recent_activity(self, info, user_id):
        transaction_query = Transaction.get_query(info)
        friendship1_query = Friendship.get_query(info)
        friendship2_query = Friendship.get_query(info)

        transactions = transaction_query.filter(
            TransactionModel.user_id == user_id
        )
        friends1 = friendship1_query.filter(
            FriendshipModel.friend1_id == user_id)
        friends2 = friendship2_query.filter(
            FriendshipModel.friend2_id == user_id)
        return [*transactions, *friends1, *friends2]

    @jwt_required
    def resolve_active_transactions(self, info, user_id):
        transaction_query = Transaction.get_query(info)
        return transaction_query.filter(TransactionModel.user_id == user_id)

    @jwt_required
    def resolve_get_expense_comments(self, info, expense_id):
        comment_query = Comment.get_query(info)
        return comment_query.filter(CommentModel.expense_id == expense_id)

    @jwt_required
    def resolve_get_expense_transactions(self, info, expense_id):
        transaction_query = Transaction.get_query(info)
        return transaction_query.filter(TransactionModel.expense_id == expense_id)

    @jwt_required
    def resolve_get_all_users(self, info, **kwargs):
        users_query = User.get_query(info)
        return users_query.all()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    create_expense = CreateExpense.Field()
    # create_group = CreateGroup.Field()
    friendship_request = FriendshipRequest.Field()
    create_transaction = CreateTransaction.Field()
    handle_friend_request = HandleFriendRequest.Field()
    create_comment = CreateComment.Field()
    handle_transaction = HandleTransaction.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
