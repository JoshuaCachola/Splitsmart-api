import graphene
import datetime

from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Friendship as FriendshipModel, Comment as CommentModel
from src import db

from src.api.schema.types import User

# import models
from src.api.users.model import User as UserModel
# from src.api.transactions.model import Transaction as TransactionModel

# import mutations
from src.api.schema.mutations import RegisterUser, CreateExpense, LoginUser


# Schema
# class Group(SQLAlchemyObjectType):
#     class Meta:
#         model = GroupModel


class Friendship(SQLAlchemyObjectType):
    class Meta:
        model = FriendshipModel


class Comment(SQLAlchemyObjectType):
    class Meta:
        model = CommentModel


# class RecentActivity(graphene.Union):
    # class Meta:
        # types = (Transaction, Friendship)


# Mutations


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


class HandleFriendRequest(graphene.Mutation):
    """
    Mutation class to change the status of a friend request
    """
    friend_request = graphene.Field(lambda: Friendship)

    class Arguments:
        id = graphene.Int(required=True)
        status = graphene.String(required=True)

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




class Query(graphene.ObjectType):
    user = graphene.Field(User, email=graphene.String())
    # get_friends = graphene.List(
        # Friendship, friend_id=graphene.Int())
    # active_expenses = graphene.List(Expense, user_id=graphene.Int())
    # recent_activity = graphene.List(RecentActivity, user_id=graphene.Int())
    # active_transactions = graphene.List(Transaction, user_id=graphene.Int())
    # get_expense_comments = graphene.List(
        # Comment, expense_id=graphene.Int())
    # get_expense_transactions = graphene.List(
        # Transaction, expense_id=graphene.Int())
    # get_all_users = graphene.List(User)
    # get_all_unpaid_transactions = graphene.List(
        # Transaction, user_id=graphene.Int())

    def resolve_user(self, info, email):
        user_query = User.get_query(info)
        user = user_query.filter(UserModel.email == email).first()
        return user if user else None

    # def resolve_get_friends(self, info, friend_id):
        # friends1_query = Friendship.get_query(info)
        # friends2_query = Friendship.get_query(info)
        # friend1 = friends1_query.filter(FriendshipModel.friend1_id == friend_id) \
            # .filter(FriendshipModel.status == 'accepted')
        # friend2 = friends2_query.filter(FriendshipModel.friend2_id == friend_id) \
            # .filter(FriendshipModel.status == 'accepted')

        # return [*friend1, *friend2]

    # def resolve_active_expenses(self, info, user_id):
        # expenses_query = Expense.get_query(info)
        # return expenses_query.filter(ExpenseModel.user_id == user_id) \
            # .filter(ExpenseModel.is_settled == False)

    # def resolve_recent_activity(self, info, user_id):
        # transaction_query = Transaction.get_query(info)
        # friendship1_query = Friendship.get_query(info)
        # friendship2_query = Friendship.get_query(info)

        # transactions = transaction_query.filter(
            # TransactionModel.user_id == user_id
        # )
        # friends1 = friendship1_query.filter(
            # FriendshipModel.friend1_id == user_id)
        # friends2 = friendship2_query.filter(
            # FriendshipModel.friend2_id == user_id)
        # return [*transactions, *friends1, *friends2]

    # def resolve_active_transactions(self, info, user_id):
        # transaction_query = Transaction.get_query(info)
        # return transaction_query.filter(TransactionModel.user_id == user_id) \
                                # .order_by(TransactionModel.updated_at.desc())

    # def resolve_get_expense_comments(self, info, expense_id):
        # comment_query = Comment.get_query(info)
        # return comment_query.filter(CommentModel.expense_id == expense_id)

    # def resolve_get_expense_transactions(self, info, expense_id):
        # transaction_query = Transaction.get_query(info)
        # return transaction_query.filter(TransactionModel.expense_id == expense_id)

    # def resolve_get_all_users(self, info, **kwargs):
        # users_query = User.get_query(info)
        # return users_query.all()

    # def resolve_get_all_unpaid_transactions(self, info, user_id):
        # transactions_query = Transaction.get_query(info)
        # return transactions_query.filter(TransactionModel.user_id == user_id) \
            # .filter(TransactionModel.is_settled == False)


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    create_expense = CreateExpense.Field()
    # create_group = CreateGroup.Field()
    # friendship_request = FriendshipRequest.Field()
    # create_transaction = CreateTransaction.Field()
    # handle_friend_request = HandleFriendRequest.Field()
    # create_comment = CreateComment.Field()
    # handle_transaction = HandleTransaction.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
