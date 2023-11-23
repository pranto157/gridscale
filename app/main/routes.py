from apiflask import APIBlueprint as Blueprint
from flask import current_app as app
from flask import jsonify


from app.errors.handlers import error_response

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return jsonify(hello="ok")


@bp.route("/log")
def log():
    app.logger.debug("This is a debug log, you can only see it when app.debug is True")
    app.logger.info("Some info")
    app.logger.warn("Warning")
    app.logger.error("Something was broken")
    return jsonify(log="ok")


@bp.route("/error/<int:code>")
def error(code):
    app.logger.error(f"Error: {code}")
    return error_response(code)
