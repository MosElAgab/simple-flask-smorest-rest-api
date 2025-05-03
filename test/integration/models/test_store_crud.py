import pytest
from sqlalchemy.exc import IntegrityError

from app.models import StoreModel, ItemModel


def test_crud_operation(session):
    """
    GIVEN a StoreModel instance
    WHEN it's added, queried, updated, and deleted from the session
    THEN the operations should reflect correct CRUD behavior
    """
    store_data = {"store_name": "my_store"}
    store = StoreModel(**store_data)
    session.add(store)
    session.commit()

    assert store.store_id is not None

    retrieved_store = StoreModel.query.filter(
        StoreModel.store_name == store_data["store_name"]
    ).first()
    assert retrieved_store.store_id == store.store_id

    # Update
    retrieved_store.store_name = "my_new_store"
    session.commit()
    updated_store = StoreModel.query.filter_by(
        store_id=retrieved_store.store_id
    ).first()
    assert updated_store.store_name == "my_new_store"

    # Delete
    session.delete(updated_store)
    session.commit()
    deleted_store = StoreModel.query.filter_by(store_id=1).first()
    assert deleted_store is None


@pytest.mark.parametrize("store_name", ["Music", "Books", "Games"])
def test_store_name_uniqueness(session, store_name):
    store_1 = StoreModel(store_name=store_name)
    store_2 = StoreModel(store_name=store_name)

    session.add(store_1)
    session.commit()
    assert store_1.store_id is not None

    session.add(store_2)
    with pytest.raises(IntegrityError):
        session.commit()


def test_store_item_relationship_link(session):
    store = StoreModel(store_name="Tesco")
    session.add(store)
    session.commit()

    item_1 = ItemModel(item_name="Milk", item_price=0.99, store_id=store.store_id)
    item_2 = ItemModel(item_name="Cheese", item_price=1.99, store_id=store.store_id)
    item_3 = ItemModel(item_name="Bread", item_price=1.49, store_id=store.store_id)
    items = [item_1, item_2, item_3]

    session.add_all(items)
    session.commit()

    assert store.items.count() == 3


def test_store_deletion_cascades_to_items(session):
    store = StoreModel(store_name="Cascade Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Mouse", item_price=49.99, store_id=store.store_id)
    session.add(item)
    session.commit()

    session.delete(store)
    session.commit()

    assert session.query(ItemModel).filter_by(store_id=store.store_id).count() == 0
