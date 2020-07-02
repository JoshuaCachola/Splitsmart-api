from flask import Flask
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from flask_cors import CORS
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
)
from flask_login import login_required, LoginManager

from .config import Config
from .models import db
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_IDENTITY_CLAIM'] = 'jti'
jwt = JWTManager(app)
# login = LoginManager(app)
# login.login_view = "session.login"
# auth = GraphQLAuth(app)
# app.config.from_object(Config)
# app.config["JWT_SECRET_KEY"] = "something"  # change this!
# app.config["REFRESH_EXP_LENGTH"] = 30
# app.config["ACCESS_EXP_LENGTH"] = 10
from .schema import schema  # noqa
cors = CORS(app, resources={r'/*': {'origin': '*'}})
app.debug = True


# def graphql_view():
#     view = GraphQLView.as_view('graphql', schema=schema, graphiql=True)
#     return jwt_required(view)

# def graphql_view():
#     view = GraphQLView.as_view('graphql', schema=schema, context={'session': db.session},
#                                graphiql=True)
#     return login_required(view)


# adds /graphql endpoint
app.add_url_rule(
    '/graphql',
    # view_func=graphql_view()
    view_func=GraphQLView.as_view('graphql', schema=schema,
                                  context={'session': db.session}, graphiql=True)

)

db.init_app(app)
Migrate(app, db)
