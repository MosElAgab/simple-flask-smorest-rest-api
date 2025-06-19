from app.models import ItemModel


def test_constructor():
    """
    GIVEN an ItemModel with required fields
    WHEN an instance is created
    THEN it should store the correct data
    """
    item = ItemModel(item_name="Metal Pipe", item_price=499.99, store_id=1)
    assert isinstance(item, ItemModel)
    assert isinstance(item.item_name, str)
    assert item.item_name == "Metal Pipe"
    assert isinstance(item.item_price, float)
    assert item.item_price == 499.99
    assert item.store_id == 1
