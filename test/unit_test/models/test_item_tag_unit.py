from app.models import ItemTagModel


def test_constructor():
    """
    GIVEN an ItemTagModel with required fields
    WHEN an instance is created
    THEN it should store the correct data
    """
    item_tag = ItemTagModel(item_id=1, tag_id=2)
    assert isinstance(item_tag, ItemTagModel)
    assert item_tag.item_id == 1
    assert isinstance(item_tag.item_id, int)
    assert item_tag.tag_id == 2
    assert isinstance(item_tag.tag_id, int)
