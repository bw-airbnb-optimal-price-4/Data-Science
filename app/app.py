# https://github.com/MLH/mlh-hackathon-flask-starter/blob/master/app/app.py

import os

from flask import Flask
from . import settings, routes
from .database import init_db, db_session
from sqlalchemy import create_engine
from decouple import config
from flask_cors import CORS

project_dir = os.path.dirname(os.path.abspath(__file__))


def create_app(config_object=settings):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    CORS(app)

    init_db()
    register_blueprints(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(routes.blueprint)
    return None
