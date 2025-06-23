import pytest

from marshmallow import ValidationError
from app.schemas import PlainItemSchema, ItemUpdateSchema, ItemSchema


## PlainItemSchema

# test valid load passed
def test_plain_item_schema_valid_load():
    schema = PlainItemSchema()
    result = schema.load({
        "item_name": "Laptop",
        "item_price": 1299.99,
        "store_id": 1
    })
    assert result["item_name"] == "Laptop"
    assert result["item_price"] == 1299.99
    assert result["store_id"] == 1


# test invalid load rejected
def test_plain_item_schema_rejects_invalid_load():
    schema = PlainItemSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({
        "item_name": "Laptop",
        "item_price": 1299.99,
        "store_id": 1,
        "invalid_field": "Store"
    })
    assert "invalid_field" in err.value.messages


# test missing required fields
def test_plain_item_schema_missing_required_fields():
    schema = PlainItemSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({})
    assert "item_name" in err.value.messages
    assert "item_price" in err.value.messages
    assert "store_id" in err.value.messages


# test invalid type rejected
def test_plain_item_schema_invalid_types():
    schema = PlainItemSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({
            "item_name": 123,
            "item_price": "2 quid",
            "store_id": "one"
        })
    assert "item_name" in err.value.messages
    assert "item_price" in err.value.messages
    assert "store_id" in err.value.messages


# test dump-only field rejected at load
def test_plain_item_schema_rejects_dump_only_on_load():
    schema = PlainItemSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({
            "item_name": "Book",
            "item_price": 9.99,
            "store_id": 2,
            "item_id": 100
        })
    assert "item_id" in err.value.messages


# test dump-only fields included at dump (SQL_Alchemy-like class)
def test_plain_item_schema_dump_includes_dump_only():
    class Item:
        def __init__(self):
            self.item_id = 10
            self.item_name = "Keyboard"
            self.item_price = 99.99
            self.store_id = 1

    schema = PlainItemSchema()
    result = schema.dump(Item())
    assert result["item_id"] == 10
    assert result["item_name"] == "Keyboard"
    assert result["item_price"] == 99.99


## ItemUpdateSchema

# test valid load passed
def test_item_update_schema_valid__load():
    schema = ItemUpdateSchema()
    result = schema.load({"item_name": "Phone"})
    assert result["item_name"] == "Phone"
    result = schema.load({"item_price": 22.5})
    assert result["item_price"] == 22.5
    result = schema.load({"item_name": "Phone"})
    assert result["item_name"] == "Phone"
    result = schema.load({"store_id": 10})
    assert result["store_id"] == 10
    result = schema.load({
        "item_name": "Phone X",
        "item_price": 900,
        "store_id": 20
    })
    assert result["item_name"] == "Phone X"
    assert result["item_price"] == 900
    assert result["store_id"] == 20


# test rejects invalid fields
def test_item_update_schema_rejects_invalid_field():
    schema = ItemUpdateSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({"invalid": "field"})
    assert "invalid" in err.value.messages


# test invalid type (e.g. int instead of str) is rejected
def test_item_update_schema_invalid_types():
    schema = ItemUpdateSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({
            "item_name": 123,
            "item_price": "2 quid",
            "store_id": "one"
        })
    assert "item_name" in err.value.messages
    assert "item_price" in err.value.messages
    assert "store_id" in err.value.messages


# test unknown field is rejected
def test_item_update_schema_rejects_unknown_field():
    schema = ItemUpdateSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({"store_id": 10, "invalid_field": "field"})
    assert "invalid_field" in err.value.messages


## ItemSchema

# test valid load (inherited from PlainItemSchema)
def test_item_schema_valid_load_from_base():
    schema = ItemSchema()
    result = schema.load({
        "item_name": "Laptop",
        "item_price": 1299.99,
        "store_id": 1
    })
    assert result["item_name"] == "Laptop"
    assert result["item_price"] == 1299.99
    assert result["store_id"] == 1


# test dump-only nested fields are rejected on load
def test_item_schema_ejects_dump_only_fields_on_load():
    schema = ItemSchema()
    with pytest.raises(ValidationError) as err:
        result = schema.load({
            "item_name": "Camera",
            "item_price": 499.99,
            "store_id": 3,
            "store": {"store_id": 1},
            "tags": [{"tag_id": 1}]
        })
    assert "store" in err.value.messages  
    assert "tags" in err.value.messages


# test dumping with nested store and tags (SQL_Alchemy-like class)
def test_item_schema_dumps_nested_fields():
    class Store:
        def __init__(self):
            self.store_id = 10
            self.store_name = "Store"

    class Tag:
        def __init__(self, tag_id, tag_name):
            self.tag_id = tag_id
            self.tag_name = tag_name

    class Item:
        def __init__(self):
            self.item_id = 5
            self.item_name = "Monitor"
            self.item_price = 159.99
            self.store = Store()
            self.tags = [Tag(1, "Electronics"), Tag(2, "Display")]

    schema = ItemSchema()
    result = schema.dump(Item())

    assert result["item_id"] == 5
    assert result["item_name"] == "Monitor"
    assert result["store"]["store_name"] == "Store"
    assert result["store"]["store_id"] == 10
    assert result["tags"][0]["tag_name"] == "Electronics"


# test dump with empty tags list (SQL_Alchemy-like class)
def test_item_schema_dumps_with_empty_nested_lists():
    class Store:
        def __init__(self):
            self.store_id = 10
            self.store_name = "Store"

    class Item:
        def __init__(self):
            self.item_id = 5
            self.item_name = "Monitor"
            self.item_price = 159.99
            self.store = Store()
            self.tags = []

    schema = ItemSchema()
    result = schema.dump(Item())
    
    assert len(result["tags"]) == 0
