from flask import Flask
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from .config import Config
from .models import db
from .schema import schema  # noqa


app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_IDENTITY_CLAIM'] = 'jti'
jwt = JWTManager(app)
cors = CORS(app, resources={r'/*': {'origin': '*'}})
app.debug = True

# adds /graphql endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema,
                                  context={'session': db.session}, graphiql=True)

)

db.init_app(app)
Migrate(app, db)
