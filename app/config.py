import os


class Config:
    SECRET_KEY: os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # JWT_ALGORITHM = 'HS256'
    # REFRESH_EXP_LENGTH = 30
    # ACCESS_EXP_LENGTH = 10
    # JWT_TOKEN_ARGUMENT_NAME = 'token'
    # JWT_TOKEN_LOCATION = 'headers'
    # JWT_HEADER_NAME = 'authorization'
