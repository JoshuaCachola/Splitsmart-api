import graphene
from decimal import Decimal
from flask_jwt_extended import create_access_token

# import object types
from .types import User, Expense

# import crud functions
from src.api.users.crud import register_user, get_user_by_email, login_user
from src.api.expense.crud import create_expense


class RegisterUser(graphene.Mutation):
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
        :rtype: { user, auth_token }
        """
        check_email = get_user_by_email(email)
        if (not check_email):
            user = register_user(first_name, last_name, email, password)
            auth_token = create_access_token(user.id)
            return RegisterUser(
                user=user,
                auth_token=auth_token
            )
        else:
            return RegisterUser(
                user=None,
                auth_token=None
            )


class LoginUser(graphene.Mutation):
    """
    Mutation class to authenticate user and create authorization token 
    """
    auth_token = graphene.String()
    user = graphene.Field(lambda: User)
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    def mutate(self, info, email, password):
        """
        email: string
        password: string
        rtype: { auth_token, user }
        """
        user = login_user(email, password)
        if user:
            auth_token = create_access_token(user.id)
            return LoginUser(
                auth_token=auth_token,
                user=user
            )
        else:
            return LoginUser(
                auth_token=None,
                user=None
            )


class CreateExpense(graphene.Mutation):
    """
    Mutation class for users to create expenses
    """
    expense = graphene.Field(lambda: Expense)

    class Arguments:
        user_id = graphene.ID(required=True)
        amount = graphene.Decimal(required=True)
        description = graphene.String(required=True)

    # @jwt_required
    def mutate(self, info, user_id, amount, description):
        """
        :type user_id: ID
        :type amount: Decimal
        :type description: string
        :rtype: CreateExpense
        """
        expense = create_expense(user_id, amount, description)
        return CreateExpense(expense=expense)
  
