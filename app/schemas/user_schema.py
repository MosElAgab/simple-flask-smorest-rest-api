from marshmallow import Schema, fields


class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)
