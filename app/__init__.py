import logging
import environ

from flask_restful import Api
from flask import Flask
from flask.logging import default_handler
from flask_migrate import Migrate
from flasgger import Swagger

from app.main.db import db
from .config import CONFIG_MAP
from .logger import get_handler
from app.views.cities import CityListView, CityView

env = environ.Env()

migrate = Migrate()


def create_app(config=None):
    # read config
    app = Flask(__name__)
    api = Api(app)
    app.config["SWAGGER"] = {"title": "Flasgger RESTful", "uiversion": 3}
    Swagger(app)

    if config is None:
        config = CONFIG_MAP[env("ENV")]

    app.config.from_object(config)

    db.init_app(app)

    # customize logger
    app.logger.removeHandler(default_handler)
    app.logger.addHandler(get_handler())
    if not app.debug:
        app.logger.setLevel(logging.INFO)
    else:
        app.logger.setLevel(logging.DEBUG)

    # disable werkzeug logger
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.disabled = True

    # import blueprints
    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    api.add_resource(CityListView, "/api/cities")
    api.add_resource(CityView, "/api/cities/<city_uuid>")

    return app
