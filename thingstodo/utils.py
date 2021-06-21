# NOTE: A place for helper utilities and decorators.

from wtoolzexceptions import exceptions
import flask
import marshmallow


def parse(schema, location):
    if location == "args":
        p = flask.request.args
    elif location == "json":
        p = flask.request.json
    elif location == "view_args":
        p = flask.request.view_args
    else:
        raise ValueError("location not args, json, or view_args.")
    try:
        return schema.load(p)
    except marshmallow.ValidationError:
        exceptions.ohoh(400)
