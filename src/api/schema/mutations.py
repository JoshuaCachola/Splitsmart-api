import graphene
from flask_jwt_extended import create_access_token

# import object types
from .types import User, Expense, Transaction, PaymentStatus

# import crud functions
from src.api.users.crud import register_user, get_user_by_email, login_user
from src.api.expenses.crud import create_expense
from src.api.transactions.crud import update_transaction


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
        first_name: string
        last_name: string
        email: string
        password: string
        rtype: RegisterUser
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
    Mutation class for users to create expenses and track transactions
    """
    expense = graphene.Field(lambda: Expense)

    class Arguments:
        user_id = graphene.ID(required=True)
        total = graphene.Decimal(required=True)
        description = graphene.String(required=True)
        transactions = graphene.JSONString(required=True)

    def mutate(self, info, user_id, total, description, transactions):
        """
        user_id: ID
        total: Decimal
        description: string
        json_input: JSONString
        rtype: CreateExpense
        """
        expense = create_expense(user_id, total, description, transactions)
        return CreateExpense(expense=expense)


class UpdateTransaction(graphene.Mutation):
    """
    Mutation class to update paying a transaction
    """
    transaction = graphene.Field(lambda: Transaction)
    error = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        status = graphene.Enum(PaymentStatus)

    def mutate(self, info, id, status):
        """
        :type id: int
        :rtype: obj
        """
        transaction = update_transaction(id, status)

        if transaction:
            return UpdateTransaction(
                transaction=transaction,
                error=""
            )
        return UpdateTransaction(
                transaction=None,
                error='''
                Error handling transaction. Charges have not taken place.
                Please try again.

                '''
        )
