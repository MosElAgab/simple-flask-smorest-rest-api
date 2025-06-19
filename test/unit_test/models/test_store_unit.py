from app.models import StoreModel


def test_constructor():
    """
    GIVEN a StoreModel class with a constructor that accepts `store_name`
    WHEN a StoreModel instance is created
    THEN the instance should have the correct `store_name`
    """
    store = StoreModel(store_name="Fake Shop")
    assert isinstance(store, StoreModel)
    assert store.store_name == "Fake Shop"
    assert isinstance(store.store_name, str)
