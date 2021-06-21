import marshmallow

from marshmallow import fields


class ViewArgsSchema(marshmallow.Schema):
    id_ = fields.UUID(required=True)

    @marshmallow.post_load
    def post_load(self, data, **kwargs):
        data["id_"] = str(data["id_"])
        return data


class PayloadSchema(marshmallow.Schema):
    id = fields.UUID(dump_only=True)
    text = fields.Str(required=True)
    completed = fields.Bool()
    date = fields.Str(dump_only=True)


view_args_schema = ViewArgsSchema()
payload_schema = PayloadSchema()
payloads_schema = PayloadSchema(many=True)
