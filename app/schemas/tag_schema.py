from marshmallow import Schema, fields


class PlainTagSchema(Schema):
    tag_id = fields.Int(dump_only=True)
    tag_name = fields.Str(required=True)


class TagSchema(PlainTagSchema):
    store = fields.Nested("PlainStoreSchema", dump_only=True)
    items = fields.List(fields.Nested("PlainItemSchema"), dump_only=True)
