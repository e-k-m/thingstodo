from marshmallow import fields
from marshmallow import validate
import marshmallow


class ArgsSchema(marshmallow.Schema):
    page = fields.Integer(
        missing=1, validate=validate.Range(min=1, max=2147483647)
    )
    limit = fields.Integer(
        missing=100, validate=validate.Range(min=1, max=100)
    )
    count = fields.Bool(missing=False)
    filter = fields.Str(missing=None)
    order = fields.Str(missing=None)


args_schema = ArgsSchema()
