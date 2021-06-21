from wtoolzexceptions import exceptions
import flask
import flask_jwt_extended as jwt
import wtoolzargs


from thingstodo.todos import models
from thingstodo.todos import serializers as s
from thingstodo import serializers
from thingstodo import utils

blueprint = flask.Blueprint("todos", __name__)


@blueprint.route("/api/v0.0/todos", methods=("GET",))
@jwt.jwt_required
def get_todos():
    args = utils.parse(serializers.args_schema, "args")
    user = jwt.get_jwt_identity()

    query = models.Todo.query.filter(models.Todo.user == user)

    if args["filter"]:
        try:
            f = wtoolzargs.filter_(models.Todo, args["filter"])
        except wtoolzargs.wtoolzargsError:
            exceptions.ohoh(400)
        query = query.filter(f)
    if args["order"]:
        try:
            o = wtoolzargs.order(models.Todo, args["order"])
        except wtoolzargs.wtoolzargsError:
            exceptions.ohoh(400)
        query = query.order_by(*o)
    page = query.paginate(args["page"], args["limit"], None)
    items, count = page.items, page.total

    res = {
        "value": s.payloads_schema.dump(items),
        "next": flask.url_for("todos.get_todos", **args),
    }
    if args["count"]:
        res["count"] = count

    return res, 200


@blueprint.route("/api/v0.0/todos", methods=("POST",))
@jwt.jwt_required
def post_todos():
    payload = utils.parse(s.payload_schema, "json")
    user = jwt.get_jwt_identity()

    res = models.Todo(payload["text"], user)
    res.save()
    return (
        s.payload_schema.dump(res),
        201,
        {"Location": flask.url_for("todos.get_todo", id_=res.id)},
    )


@blueprint.route("/api/v0.0/todos/<id_>", methods=("GET",))
@jwt.jwt_required
def get_todo(id_):
    args = utils.parse(s.view_args_schema, "view_args")
    user = jwt.get_jwt_identity()

    res = models.Todo.query.get(args["id_"])
    if not res:
        exceptions.ohoh(404)
    # FIXME: review right code-
    if res.user != user:
        exceptions.ohoh(403)
    return s.payload_schema.dump(res), 200


@blueprint.route("/api/v0.0/todos/<id_>", methods=("PUT",))
@jwt.jwt_required
def put_todo(id_):
    args = utils.parse(s.view_args_schema, "view_args")
    user = jwt.get_jwt_identity()

    res = models.Todo.query.get(args["id_"])
    if not res:
        exceptions.ohoh(404)
    # FIXME: review right code.
    if res.user != user:
        exceptions.ohoh(403)
    payload = utils.parse(s.payload_schema, "json")

    res.update(**payload)
    res.save()

    return s.payload_schema.dump(res), 201


@blueprint.route("/api/v0.0/todos/<id_>", methods=("DELETE",))
@jwt.jwt_required
def delete_todo(id_):
    args = utils.parse(s.view_args_schema, "view_args")
    user = jwt.get_jwt_identity()

    res = models.Todo.query.get(args["id_"])
    if not res:
        exceptions.ohoh(404)
    # FIXME: review right code
    if res.user != user:
        exceptions.ohoh(403)
    res.delete()
    return "", 204
