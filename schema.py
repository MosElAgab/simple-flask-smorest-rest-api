from marshmallow import Schema, fields


class PlainStoreSchema(Schema):
    store_id = fields.Int(dump_only=True)
    store_name = fields.Str(required=True)


class StoreUpdateSchema(Schema):
    store_name = fields.Str(required=True)


class PlainItemSchema(Schema):
    item_id = fields.Int(dump_only=True)
    item_name = fields.Str(required=True)
    item_price = fields.Float(required=True)
    store_id = fields.Int(required=True, load_only=True)


class ItemUpdateSchema(Schema):
    item_name = fields.Str()
    item_price = fields.Float()
    store_id = fields.Int()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class ItemSchema(PlainItemSchema):
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
