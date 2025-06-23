import pytest
from marshmallow import ValidationError
from app.schemas import PlainStoreSchema


# PlainStoreSchema
# test valid load passed
def test_PlainStoreSchema_valid_load():
    schema = PlainStoreSchema()
    result = schema.load({"store_name": "Store"})
    assert result["store_name"] == "Store"


# test invalid load rejected
def test_PlainStoreSchema_rejects_invalid_load():
    schema = PlainStoreSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({"invalid_field": "Store"})
    assert "invalid_field" in err.value.messages


# test missing required fields
def test_PlainStoreSchema_missing_required_fields():
    schema = PlainStoreSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({})
    assert "store_name" in err.value.messages


# test invalid type rejected
def test_PlainStoreSchema_invalid_type():
    schema = PlainStoreSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({"store_name": 2})
    assert "store_name" in err.value.messages


# test dump-only field ignored at load
def test_PlainStoreSchema_rejects_dump_only_fields_at_load():
    schema = PlainStoreSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({
            "store_name": "Store",
            "store_id": 2
        })
    assert "store_id" in err.value.messages


# test dump-only fields included at dump
def test_plain_store_schema_dump_includes_dump_only_fields():
    schema = PlainStoreSchema()
    result = schema.dump({"store_id": 1, "store_name": "Store"})
    assert result["store_id"] == 1
    assert result["store_name"] == "Store"
