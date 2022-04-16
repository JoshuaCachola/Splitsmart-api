import os

from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


# instantiate extensions
jwt_manager = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()


def create_app(script_info=None):
    # instantiate app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt_manager.init_app(app)

    # import blueprints
    from src.api.ping import ping_blueprint

    # register blueprints
    app.register_blueprint(ping_blueprint)

    # import schema
    from src.schema import schema    

    # adds /graphql endpoint
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)

    )

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app

