from marshmallow import Schema, fields


class PlainStoreSchema(Schema):
    store_id = fields.Int(dump_only=True)
    store_name = fields.Str(required=True)


class StoreUpdateSchema(Schema):
    store_name = fields.Str(required=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested("PlainItemSchema"), dump_only=True)
    tags = fields.List(fields.Nested("PlainTagSchema"), dump_only=True)
