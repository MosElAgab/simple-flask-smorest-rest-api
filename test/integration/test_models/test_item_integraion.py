import pytest
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from app.models import ItemModel, StoreModel, TagModel


# test crud operation (create, retieve, update and delete)
def test_item_crud_operations(session):
    """
    GIVEN a StoreModel and an ItemModel
    WHEN item is added, queried, updated, and deleted
    THEN all operations should work as expected
    """
    # create
    store = StoreModel(store_name="Daaz")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Metal Pipe", item_price=899.99, store_id=store.store_id)
    session.add(item)
    session.commit()

    assert item.item_id is not None

    # retrieve
    retrieved = session.query(ItemModel).filter_by(item_id=item.item_id).first()
    assert retrieved.item_name == "Metal Pipe"
    assert retrieved.item_price == 899.99
    assert retrieved.store_id == store.store_id
    assert item.store.store_name == "Daaz"

    # Update
    retrieved.item_name = "Metal Sheet"
    retrieved.item_price = 799.99
    session.commit()
    updated = session.query(ItemModel).filter_by(item_id=item.item_id).first()
    assert updated.item_name == "Metal Sheet"
    assert updated.item_price == 799.99

    # Delete
    session.delete(updated)
    session.commit()
    deleted = session.query(ItemModel).filter_by(item_id=item.item_id).first()
    assert deleted is None


# test item creation require a store for allocation
def test_item_requires_store(session):
    """
    GIVEN an ItemModel with no valid store_id
    WHEN it's added to the session
    THEN an IntegrityError should be raised
    """
    item = ItemModel(
        item_name="Keyboard", item_price=199.99, store_id=99999
    )  # Invalid FK
    session.add(item)
    with pytest.raises(IntegrityError):
        session.commit()


# test Field nullability
@pytest.mark.parametrize("item_data", [
    {"item_price": 19.99, "store_id": 1},  # missing item_name
    {"item_name": "Test Item", "store_id": 1},  # missing item_price
    {"item_name": "Test Item", "item_price": 19.99}  # missing store_id
])
def test_item_required_fields(session, item_data):
    store = StoreModel(store_name="Store", store_id=1)
    session.add(store)
    session.commit()

    item = ItemModel(**item_data)
    session.add(item)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


# test item-store relationship (store reference to the item can be retrieved)
def test_item_store_relationship_link(session):
    store = StoreModel(store_name="My Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Milk", item_price=0.99, store_id=store.store_id)
    session.add(item)
    session.commit()

    assert item.store.store_name == store.store_name


# test the uniquness of items within a store
def test_duplicate_item_name_in_same_store_not_allowed(session):
    """
    GIVEN two ItemModel instances with the same name in the same store
    WHEN both are added to the session
    THEN an IntegrityError should be raised due to the unique constraint
    """
    store = StoreModel(store_name="Tool Shop")
    session.add(store)
    session.commit()

    item1 = ItemModel(item_name="Hammer", item_price=15.99, store_id=store.store_id)
    item2 = ItemModel(item_name="Hammer", item_price=17.99, store_id=store.store_id)

    session.add(item1)
    session.commit()

    session.add(item2)
    with pytest.raises(IntegrityError):
        session.commit()


# test cross-store duplication allowance
def test_items_with_same_name_can_exist_in_different_stores(session):
    store1 = StoreModel(store_name="Store A")
    store2 = StoreModel(store_name="Store B")
    session.add_all([store1, store2])
    session.commit()

    item1 = ItemModel(item_name="AK 47", item_price=5.99, store_id=store1.store_id)
    item2 = ItemModel(item_name="AK 47", item_price=6.49, store_id=store2.store_id)
    session.add_all([item1, item2])
    session.commit()

    assert item1.item_name == item2.item_name
    assert item1.store_id != item2.store_id


# test item-tag relationship (tag referenced to the item can be retrieved)
def test_item_tag_relationship(session):
    store = StoreModel(store_name="Tagged Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Soda", item_price=1.99, store_id=store.store_id)
    session.add(item)
    session.commit()

    tag = TagModel(tag_name="Beverages", store_id=store.store_id)
    session.add(tag)
    session.commit()

    item.tags.append(tag)
    session.commit()

    assert tag in item.tags
    assert item in tag.items


# test item-tag relationship many-to-many item can have many tags
def test_item_can_have_multiple_tags(session):
    store = StoreModel(store_name="Multi-Tag Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Red Bull", item_price=2.49, store_id=store.store_id)
    session.add(item)
    session.commit()

    tag1 = TagModel(tag_name="Drinks", store_id=store.store_id)
    tag2 = TagModel(tag_name="Energy", store_id=store.store_id)
    session.add_all([tag1, tag2])
    session.commit()

    item.tags.extend([tag1, tag2])
    session.commit()

    tag_names = [tag.tag_name for tag in item.tags]
    assert set(tag_names) == {"Drinks", "Energy"}


# test item can have zero tags
def test_item_can_have_no_tags(session):
    store = StoreModel(store_name="Untagged Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Plain Water", item_price=0.99, store_id=store.store_id)
    session.add(item)
    session.commit()

    assert len(item.tags) == 0


# test item cannot have duplicate tags
def test_duplicate_item_tag_pair_not_allowed(session):
    """
    GIVEN an ItemModel and a TagModel
    WHEN the same tag is assigned twice to the same item
    THEN an IntegrityError should be raised due to the unique constraint in the join table
    """
    store = StoreModel(store_name="Join Constraint Test Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Mango Juice", item_price=2.99, store_id=store.store_id)
    tag = TagModel(tag_name="Beverage", store_id=store.store_id)
    session.add_all([item, tag])
    session.commit()

    item.tags.append(tag)
    session.commit()

    item.tags.append(tag)

    with pytest.raises(IntegrityError):
        session.commit()

# test item cannot be tagged with a tag in different store (prevent cross-store tagging.)
# but first decide in which layer this validation fit the best (model, schema or service)
