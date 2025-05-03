import pytest
from sqlalchemy.exc import IntegrityError

from app.models import ItemModel, StoreModel

def test_item_crud_operations(session):
    """
    GIVEN a StoreModel and an ItemModel
    WHEN item is added, queried, updated, and deleted
    THEN all operations should work as expected
    """
    store = StoreModel(store_name="Daaz")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Metal Pipe", item_price=899.99, store_id=store.store_id)
    session.add(item)
    session.commit()

    assert item.item_id is not None

    retrieved = session.query(ItemModel).filter_by(item_id=item.item_id).first()
    assert retrieved.item_name == "Metal Pipe"
    assert retrieved.item_price == 899.99
    assert retrieved.store_id == store.store_id

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

def test_item_requires_fields(session):
    item = ItemModel(item_price=19.99, store_id=1)  # Missing item_name
    session.add(item)
    with pytest.raises(IntegrityError):
        session.commit()


def test_item_store_relationship_link(session):
    store = StoreModel(store_name="My Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Milk", item_price=0.99, store_id=store.store_id)
    session.add(item)
    session.commit()

    assert item.store.store_name == store.store_name


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

def test_same_item_name_different_stores(session):
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
