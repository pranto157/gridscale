import logging
import time
import environ

from apiflask import APIFlask as Flask
from flask import g, request
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy

from .config import CONFIG_MAP
from .logger import get_handler

env = environ.Env()
db = SQLAlchemy()


def create_app(config=None):
    # read config
    app = Flask(__name__)

    if config is None:
        config = CONFIG_MAP[env("ENV")]

    app.config.from_object(config)

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

    # init 3rd party flask plugins
    db.init_app(app)

    # import blueprints
    from app.errors import bp as errors_bp
    from app.main import bp as main_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)

    # setup shell context
    @app.shell_context_processor
    def make_shell_context():
        return {"db": db}

    # setup request hooks
    @app.before_request
    def before_req():
        g.start = time.time()

    @app.after_request
    def after_req(response):
        ms_passed = (time.time() - g.start) * 1000
        path = f'{response.status_code} "{request.method} {request.path}"'
        log = f"{request.remote_addr} ===> {path}  🕒 {ms_passed:.2f} ms"
        app.logger.info(log)
        return response

    return app


# from app.models import models  # noqa
