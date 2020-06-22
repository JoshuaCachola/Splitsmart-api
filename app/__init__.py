from flask import Flask
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from flask_cors import CORS

from .config import Config
from .models import db
from .schema import schema, User


app = Flask(__name__)
app.debug = True
app.config.from_object(Config)


# adds /graphql endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


cors = CORS(app, resources={r'/*': {'origin': '*'}})
db.init_app(app)
Migrate(app, db)
