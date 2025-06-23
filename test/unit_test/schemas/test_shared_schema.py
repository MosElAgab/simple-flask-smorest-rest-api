import pytest

from app.schemas import TagAndItemSchema


# test valid dump with nested item and tag (SQLAlchemy-like classes)
def test_tag_and_item_schema_dump():
    class Item:
        def __init__(self):
            self.item_id = 1
            self.item_name = "Speaker"
            self.item_price = 49.99
            self.store_id = 2

    class Tag:
        def __init__(self):
            self.tag_id = 3
            self.tag_name = "Electronics"

    class Response:
        def __init__(self):
            self.message = "Tag was unlinked from item successfully"
            self.item = Item()
            self.tag = Tag()

    schema = TagAndItemSchema()
    result = schema.dump(Response())

    assert result["message"] == "Tag was unlinked from item successfully"
    assert result["item"]["item_name"] == "Speaker"
    assert result["item"]["item_price"] == 49.99
    assert result["tag"]["tag_name"] == "Electronics"


# test load should reject all fields (since all are dump_only)
def test_tag_and_item_schema_rejects_all_fields_on_load():
    schema = TagAndItemSchema()
    with pytest.raises(Exception):  # could use ValidationError explicitly
        schema.load({
            "message": "Not allowed",
            "item": {"item_name": "Tablet"},
            "tag": {"tag_name": "Tech"}
        })
