import os

import flask
import werkzeug.exceptions
import wtoolzexceptions.exceptions

from thingstodo import database
from thingstodo import extensions
from thingstodo import log
from thingstodo import settings
from thingstodo import todos

import thingstodo.todos.views  # noqa


def create_app(configuration=settings.ProdConfig):
    app = flask.Flask(__name__.split(".")[0])
    register_configuration(app, configuration)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_error_handler(app)
    register_openapi(app)
    return app


def register_configuration(app, configuration):
    app.config.from_object(configuration)
    app.url_map.strict_slashes = True


def register_extensions(app):
    extensions.db.init_app(app)
    extensions.migrate.init_app(app)
    extensions.cors.init_app(app, origins=app.config["CORS_ORIGIN_WHITELIST"])
    extensions.jwt.init_app(app)
    log.init_app(app)


def register_blueprints(app):
    app.register_blueprint(todos.views.blueprint)


def register_error_handler(app):
    def response(e):
        resp = flask.jsonify(e.to_dict())
        resp.status_code = e.http_status_code
        return resp

    def log_error(e):
        log.logger.exception("exception.1")

    def handle_exception(e):
        if isinstance(e, werkzeug.exceptions.HTTPException):
            if e.code >= 500:
                log_error(e)
            try:
                wtoolzexceptions.exceptions.ohoh(e.code)
            except wtoolzexceptions.exceptions.HTTPException as e:
                return response(e)
        if isinstance(e, wtoolzexceptions.exceptions.HTTPException):
            if e.http_status_code >= 500:
                log_error(e)
            return response(e)
        log_error(e)
        # FIXME: Review error bubbling in testing, else change back to
        # how it was.
        return response(wtoolzexceptions.exceptions.InternalServerError())

    app.register_error_handler(Exception, handle_exception)


def register_shell_context(app):
    def shell_context():
        return {
            "db": database.db,
            "Todo": todos.models.Todo,
        }

    app.shell_context_processor(shell_context)


def register_openapi(app):
    def get_openapi():
        p = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "static/openapi.yml"
        )
        return flask.send_file(p, "text/x-yaml")

    app.add_url_rule("/api/v0.0/openapi.yml", "get_openapi", get_openapi)
