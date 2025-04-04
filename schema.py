from marshmallow import Schema, fields

class StoreSchema(Schema):
    store_id = fields.Str(dump_only=True)
    store_name = fields.Str(required=True)
