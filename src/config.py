import os
from datetime import timedelta


class BaseConfig:
    """
    Base Configuration
    """
    Testing = False
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    BCRYPT_LOG_ROUNDS = 13
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=14)
    # JWT_ALGORITHM = 'HS256'
    # REFRESH_EXP_LENGTH = 30
    # ACCESS_EXP_LENGTH = 10
    # JWT_TOKEN_ARGUMENT_NAME = 'token'
    # JWT_TOKEN_LOCATION = 'headers'
    # JWT_HEADER_NAME = 'authorization'


class DevelopmentConfig(BaseConfig):
    """
    Development Configuration
    """
    pass

class TestConfig(BaseConfig):
    """
    Testing configuration
    """
    TESTING = True
    JWT_SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    BCRYPT_LOG_ROUNDS = 4
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=5)


class ProductionConfig(BaseConfig):
    """
    Production configuration
    """
    pass
