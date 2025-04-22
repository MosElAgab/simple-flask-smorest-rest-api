from marshmallow import Schema, fields


class StoreSchema(Schema):
    store_id = fields.Int(dump_only=True)
    store_name = fields.Str(required=True)


class StoreUpdateSchema(Schema):
    store_name = fields.Str(required=True)

class ItemSchema(Schema):
    item_id = fields.Str(dump_only=True)
    item_name = fields.Str(required=True)
    item_price = fields.Float(required=True)
    store_id = fields.Int(required=True)


class ItemUpdateSchema(Schema):
    item_name = fields.Str()
    item_price = fields.Float()
    store_id = fields.Int()