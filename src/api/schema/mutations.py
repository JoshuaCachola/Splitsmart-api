import graphene
from flask_jwt_extended import create_access_token

# import object types
from .types import User, Expense

# import crud functions
from src.api.users.crud import register_user, get_user_by_email, login_user
from src.api.expenses.crud import create_expense


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


# class HandleTransaction(graphene.Mutation):
    # """
    # Mutation class to handle paying a transaction
    # """
    # transaction = graphene.Field(lambda: Transaction)

    # class Arguments:
        # id = graphene.Int(required=True)

    # def mutate(self, info, id):
        # """
        # :type id: int
        # :rtype: obj
        # """
        # transaction = TransactionModel.query.filter_by(id=id).first()
        # transaction.paid_on = datetime.datetime.now()
        # transaction.updated_at = datetime.datetime.now()
        # transaction.is_settled = True
        # db.session.commit()
        # return HandleTransaction(transaction=transaction)
