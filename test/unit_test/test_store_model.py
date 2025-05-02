import pytest
from sqlalchemy.exc import IntegrityError

from app.models import StoreModel


def test_constructor():
    """
    GIVEN a StoreModel class with a constructor that accepts `store_name`
    WHEN a StoreModel instance is created
    THEN the instance should have the correct `store_name`
    """
    store = StoreModel(store_name="Fake Shop")
    assert store.store_name == "Fake Shop"


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

    retrieved_store.store_name = "my_new_store"
    session.commit()
    updated_store = StoreModel.query.filter_by(store_id=1).first()
    assert updated_store.store_name == "my_new_store"

    session.delete(updated_store)
    session.commit()
    deleted_store = StoreModel.query.filter_by(store_id=1).first()
    assert deleted_store is None


def test_store_name_uniqueness(session):
    store_name = "Music"
    store_1 = StoreModel(store_name=store_name)
    store_2 = StoreModel(store_name=store_name)

    session.add(store_1)
    session.commit()

    session.add(store_2)
    with pytest.raises(IntegrityError):
        session.commit()
