from app.models import TagModel


def test_constructor():
    """
    GIVEN a TagModel with required fields
    WHEN an instance is created
    THEN it should store the correct data
    """
    tag = TagModel(tag_name="Drinks", store_id=1)
    assert isinstance(tag, TagModel)
    assert tag.tag_name == "Drinks"
    assert tag.store_id == 1
