import pytest
from marshmallow import ValidationError

from app.schemas import PlainStoreSchema, StoreUpdateSchema, StoreSchema


## PlainStoreSchema
# test valid load passed
def test_plain_store_schema_valid_load():
    schema = PlainStoreSchema()
    result = schema.load({"store_name": "Store"})
    assert result["store_name"] == "Store"


# test invalid load rejected
def test_plain_store_schema_rejects_invalid_load():
    schema = PlainStoreSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({"invalid_field": "Store"})
    assert "invalid_field" in err.value.messages


# test missing required fields
def test_plain_store_schema_missing_required_fields():
    schema = PlainStoreSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({})
    assert "store_name" in err.value.messages


# test invalid type rejected
def test_plain_store_schema_invalid_type():
    schema = PlainStoreSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({"store_name": 2})
    assert "store_name" in err.value.messages


# test dump-only field ignored at load
def test_plain_store_schema_rejects_dump_only_fields_at_load():
    schema = PlainStoreSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({
            "store_name": "Store",
            "store_id": 2
        })
    assert "store_id" in err.value.messages


# test dump-only fields included at dump (SQL_Alchemy-like class)
def test_plain_store_schema_dump_includes_dump_only_fields():
    class Store:
        def __init__(self):
            self.store_id = 2
            self.store_name = "Store"
    schema = PlainStoreSchema()
    store = Store()
    result = schema.dump(store)
    assert result["store_id"] == 2
    assert result["store_name"] == "Store"


## UpdateStoreSchema
# test valid load passed
def test_store_update_schema_valid_load():
    schema = StoreUpdateSchema()
    result = schema.load({"store_name": "Updated Store"})
    assert result["store_name"] == "Updated Store"


# test missing required field is rejected
def test_store_update_schema_missing_store_name():
    schema = StoreUpdateSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({})
    assert "store_name" in err.value.messages


# test invalid type (e.g. int instead of str) is rejected
def test_store_update_schema_invalid_type():
    schema = StoreUpdateSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({"store_name": 123})
    assert "store_name" in err.value.messages


# test unknown field is rejected
def test_store_update_schema_rejects_unknown_field():
    schema = StoreUpdateSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({"store_name": "Test", "invalid_field": "field"})
    assert "invalid_field" in err.value.messages


## StoreSchema
# test valid input using only base field (inherited from PlainStoreSchema)
def test_store_schema_valid_load_from_base():
    schema = StoreSchema()
    result = schema.load({"store_name": "My Store"})
    assert result["store_name"] == "My Store"


# test dump-only nested fields are rejected on load
def test_store_schema_rejects_dump_only_fields_on_load():
    schema = StoreSchema()
    data = {
        "store_name": "My Store",
        "items": [{"item_name": "Milk"}],
        "tags": [{"tag_name": "Grocery"}],
    }
    with pytest.raises(ValidationError) as err:
        result = schema.load(data)


# test dumping a store with nested items and tags (SQL_Alchemy-like class)
def test_store_schema_dumps_nested_fields():
    class Item:
        def __init__(self, item_id, item_name, item_price):
            self.item_id = item_id
            self.item_name = item_name
            self.item_price = item_price

    class Tag:
        def __init__(self, tag_id, tag_name):
            self.tag_id = tag_id
            self.tag_name = tag_name

    class Store:
        def __init__(self):
            self.store_id = 1
            self.store_name = "Store"
            self.items = [Item(1, "Milk", 2.5), Item(2, "Bread", 1.0)]
            self.tags = [Tag(1, "Dairy"), Tag(2, "Bakery")]

    schema = StoreSchema()
    result = schema.dump(Store())

    assert result["store_id"] == 1
    assert result["store_name"] == "Store"
    assert isinstance(result["items"], list)
    assert result["items"][0]["item_name"] == "Milk"
    assert result["tags"][1]["tag_name"] == "Bakery"


# test dump with empty items and tags lists (SQL_Alchemy-like class)
def test_store_schema_dumps_with_empty_nested_lists():
    class Store:
        def __init__(self):
            self.store_id = 2
            self.store_name = "Empty store"
            self.items = []
            self.tags = []

    schema = StoreSchema()
    result = schema.dump(Store())

    assert result["store_id"] == 2
    assert result["store_name"] == "Empty store"
    assert len(result["items"]) == 0
    assert len(result["tags"]) == 0
