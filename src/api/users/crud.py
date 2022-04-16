from src import db
from .model import User


# create
def register_user(first_name, last_name, email, password):
    """
    first_name: String
    last_name : String
    email     : String
    password  : String
    rType     : User
    """

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    
    db.session.add(user)
    db.session.commit()
    return user


# read
def get_user_by_email(email):
    """
    email: String
    rType: User
    """
    return User.query.filter_by(email=email).first()


def login_user(email, password):
    """
    email   : String
    password: String
    rType   : User
    """
    user = User.query.filter_by(email=email).first()
    if (user and user.check_password(password)):
        return user
    return None


