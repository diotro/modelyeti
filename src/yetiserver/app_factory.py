"""The application factory, which produces application servers. See
http://flask.pocoo.org/docs/1.0/patterns/appfactories
for more details."""
import json

from flask import Flask


def create_app(database_credentials):
    """Creates a flask application.

    :param database_credentials: the database credentials.
    :return: the app
    """
    app = Flask(__name__)

    from yetiserver.database import connect_to_database
    app.db = connect_to_database(database_credentials)

    from yetiserver.authentication import auth_manager_from_redis_connection
    app.auth = auth_manager_from_redis_connection(app.db)

    from yetiserver.model import model_manager_from_redis_conn
    app.model = model_manager_from_redis_conn(app.db)

    from yetiserver.model_log import model_log_from_redis_conn
    app.model_log = model_log_from_redis_conn(app.db)

    from yetiserver.api.v1 import register_api_blueprints
    register_api_blueprints(app)



    return app


def create_app_from_file(database_credentials_file):
    with open(database_credentials_file, 'r') as file:
        return create_app(json.load(file))