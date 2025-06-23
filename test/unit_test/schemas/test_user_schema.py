import pytest

from marshmallow import ValidationError
from app.schemas import UserSchema


# test valid load passed
def test_user_schema_valid_load():
    schema = UserSchema()
    result = schema.load({
        "username": "john_doe",
        "password": "123456"
    })
    assert result["username"] == "john_doe"
    assert result["password"] == "123456"


# test missing required field
def test_user_schema_missing_required_username():
    schema = UserSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({"password": "secret"})
    assert "username" in err.value.messages


# test password is required
def test_user_schema_missing_password():
    schema = UserSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({"username": "missing_password"})
    assert "password" in err.value.messages


# test invalid type
def test_user_schema_invalid_username_type():
    schema = UserSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({"username": 123, "password": 123456})
    assert "username" in err.value.messages
    assert "password" in err.value.messages

# test unknown field rejected
def test_user_schema_rejects_unknown_field():
    schema = UserSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({"username": "john", "password": "pwd", "is_admin": "admin"})
    assert "is_admin" in err.value.messages


# test dump includes user_id but excludes password (SQLAlchemy-like object)
def test_user_schema_dump_includes_user_id_only():
    class User:
        def __init__(self):
            self.user_id = 1
            self.username = "john_doe"
            self.password = "my_password"

    schema = UserSchema()
    result = schema.dump(User())
    assert result["user_id"] == 1
    assert result["username"] == "john_doe"
    assert "password" not in result
