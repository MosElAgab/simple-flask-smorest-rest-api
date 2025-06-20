from marshmallow import Schema, fields


class TagAndItemSchema(Schema):
    message = fields.Str(dump_only=True)
    item = fields.Nested("PlainItemSchema", dump_only=True)
    tag = fields.Nested("PlainTagSchema", dump_only=True)
