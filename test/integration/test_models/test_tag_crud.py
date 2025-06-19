import pytest
from sqlalchemy.exc import IntegrityError

from app.models import TagModel, StoreModel, ItemModel


# test crud operation (create, retieve, update and delete)
def test_tag_crud_operations(session):
    """
    GIVEN a TagModel instance
    WHEN it is created, queried, updated, and deleted
    THEN the operations should behave as expected
    """

    # create
    store = StoreModel(store_name="Some Store")
    session.add(store)
    session.commit()

    tag = TagModel(tag_name="Electronics", store_id=store.store_id)
    session.add(tag)
    session.commit()

    assert tag.tag_id is not None

    # Query
    retrieved = session.query(TagModel).filter_by(tag_id=tag.tag_id).first()
    assert retrieved.tag_name == "Electronics"

    # Update
    retrieved.tag_name = "Home"
    session.commit()

    updated = session.query(TagModel).filter_by(tag_id=tag.tag_id).first()
    assert updated.tag_name == "Home"

    # Delete
    session.delete(updated)
    session.commit()
    assert session.query(TagModel).filter_by(tag_id=tag.tag_id).first() is None


# test Field nullability
@pytest.mark.parametrize("tag_data", [
    {"store_id": 1},
    {"tag_name": "Electronics"}
])
def test_tag_required_fields(session, tag_data):
    """
    GIVEN a TagModel
    WHEN tag_name or store_id is missing
    THEN an IntegrityError should be raised due to null constraint
    """
    store = StoreModel(store_name="Store", store_id=1)
    session.add(store)
    session.commit()

    tag = TagModel(**tag_data)
    session.add(tag)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

   
# test tag creation require a store for allocation
def test_tag_requires_store(session):
    """
    GIVEN an TagModel with no valid store_id
    WHEN it's added to the session
    THEN an IntegrityError should be raised
    """
    tag = TagModel(tag_name="Electronics", store_id=99999)# Invalid FK
    session.add(tag)
    with pytest.raises(IntegrityError):
        session.commit()


# test the uniquness of tags within a store
def test_duplicate_tag_in_same_store_not_allowed(session):
    """
    GIVEN a StoreModel and two TagModel instances with the same name
    WHEN both tags are assigned to the same store
    THEN the database should raise an IntegrityError due to the unique constraint
    """
    store = StoreModel(store_name="Movie")
    session.add(store)
    session.commit()

    tag1 = TagModel(tag_name="Fiction", store_id=store.store_id)
    tag2 = TagModel(tag_name="Fiction", store_id=store.store_id)

    session.add(tag1)
    session.commit()

    session.add(tag2)
    with pytest.raises(IntegrityError):
        session.commit()


# test same tag name different store is allowed
def test_same_tag_name_in_different_stores_allowed(session):
    """
    GIVEN two StoreModel instances
    AND TagModel instances with the same tag_name in different stores
    WHEN both are added to the session
    THEN the database should allow it without raising an IntegrityError
    """
    store1 = StoreModel(store_name="Tesco")
    store2 = StoreModel(store_name="Asda")
    session.add_all([store1, store2])
    session.commit()

    tag1 = TagModel(tag_name="Drinks", store_id=store1.store_id)
    tag2 = TagModel(tag_name="Drinks", store_id=store2.store_id)

    session.add_all([tag1, tag2])
    session.commit()  # Should not raise IntegrityError

    assert tag1.tag_id is not None
    assert tag2.tag_id is not None
    assert tag1.store_id != tag2.store_id


# test tag store relationship link
def test_tag_store_relationship_link(session):
    """
    GIVEN a TagModel linked to a StoreModel via store_id
    WHEN the tag is committed
    THEN the tag's store relationship should correctly return the associated StoreModel
    """
    store = StoreModel(store_name="My Store")
    session.add(store)
    session.commit()

    tag = TagModel(tag_name="Clearance", store_id=store.store_id)
    session.add(tag)
    session.commit()

    assert tag.store is not None
    assert tag.store.store_id == store.store_id
    assert tag.store.store_name == "My Store"


# test tag can have no items
def test_tag_with_no_items(session):
    store = StoreModel(store_name="Empty Tags")
    session.add(store)
    session.commit()

    tag = TagModel(tag_name="Unused", store_id=store.store_id)
    session.add(tag)
    session.commit()

    assert len(tag.items) == 0


# test item-tag relationship many-to-many tag can have many items
def test_tag_can_have_many_items(session):
    """
    GIVEN a TagModel and multiple ItemModel instances in the same store
    WHEN the tag is assigned to multiple items
    THEN tag.items should contain all associated items
    """
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    item1 = ItemModel(item_name="Shirt", item_price=15.99, store_id=store.store_id)
    item2 = ItemModel(item_name="Jeans", item_price=39.99, store_id=store.store_id)
    tag = TagModel(tag_name="Clothing", store_id=store.store_id)

    session.add_all([item1, item2, tag])
    session.commit()

    # Associate tag with both items
    tag.items.extend([item1, item2])
    session.commit()

    item_names = [item.item_name for item in tag.items]
    assert set(item_names) == {"Shirt", "Jeans"}
