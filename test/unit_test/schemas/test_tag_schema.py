import pytest

from marshmallow import ValidationError
from app.schemas import PlainTagSchema, TagSchema


## PlainTagSchema

# test valid load passed
def test_plain_tag_schema_valid_load():
    schema = PlainTagSchema()
    result = schema.load({"tag_name": "Electronics"})
    assert result["tag_name"] == "Electronics"


# test missing required field
def test_plain_tag_schema_missing_required_field():
    schema = PlainTagSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({})
    assert "tag_name" in err.value.messages


# test invalid type rejected
def test_plain_tag_schema_invalid_type():
    schema = PlainTagSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({"tag_name": 123})
    assert "tag_name" in err.value.messages


# test unknown field is rejected
def test_plain_tag_schema_rejects_unknown_field():
    schema = PlainTagSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({"tag_name": "Sale", "invalid_field": "unexpected"})
    assert "invalid_field" in err.value.messages


# test dump includes dump-only field (SQLAlchemy-like class)
def test_plain_tag_schema_dump_includes_dump_only():
    class Tag:
        def __init__(self):
            self.tag_id = 1
            self.tag_name = "Seasonal"

    schema = PlainTagSchema()
    result = schema.dump(Tag())
    assert result["tag_id"] == 1
    assert result["tag_name"] == "Seasonal"


## TagSchema

# test valid load inherited from PlainTagSchema
def test_tag_schema_valid_load_from_base():
    schema = TagSchema()
    result = schema.load({"tag_name": "Discount"})
    assert result["tag_name"] == "Discount"


# test dump-only nested fields are rejected on load
def test_tag_schema_rejects_dump_only_nested_fields_on_load():
    schema = TagSchema()
    with pytest.raises(ValidationError) as err:
        schema.load({
            "tag_name": "Popular",
            "store": {"store_name": "Tech Store"},
            "items": [{"item_name": "Headphones"}]
        })
    assert "store" in err.value.messages
    assert "items" in err.value.messages


# test dumping with nested store and items (SQLAlchemy-like class)
def test_tag_schema_dumps_nested_fields():
    class Store:
        def __init__(self):
            self.store_id = 10
            self.store_name = "Tech Store"

    class Item:
        def __init__(self, item_id, item_name, item_price):
            self.item_id = item_id
            self.item_name = item_name
            self.item_price = item_price

    class Tag:
        def __init__(self):
            self.tag_id = 5
            self.tag_name = "Popular"
            self.store = Store()
            self.items = [Item(1, "Phone", 699), Item(2, "Tablet", 499)]

    schema = TagSchema()
    result = schema.dump(Tag())

    assert result["tag_id"] == 5
    assert result["tag_name"] == "Popular"
    assert result["store"]["store_name"] == "Tech Store"
    assert isinstance(result["items"], list)
    assert result["items"][0]["item_name"] == "Phone"


# test dumping with empty nested items
def test_tag_schema_dumps_with_empty_nested_items():
    class Store:
        def __init__(self):
            self.store_id = 10
            self.store_name = "Tech Store"

    class Tag:
        def __init__(self):
            self.tag_id = 6
            self.tag_name = "Empty"
            self.store = Store()
            self.items = []

    schema = TagSchema()
    result = schema.dump(Tag())


    assert len(result["items"]) == 0
