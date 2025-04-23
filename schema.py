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


class PlainTagSchema(Schema):
    tag_id = fields.Int(dump_only=True)
    tag_name = fields.Str(required=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class ItemSchema(PlainItemSchema):
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    # store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
