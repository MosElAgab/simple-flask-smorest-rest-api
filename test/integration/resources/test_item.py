import pytest

from app.models import ItemModel, StoreModel


## /item

# test get with no data
def test_get_item_list_returns_empty(client):
    response = client.get("/item")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.json == []


# test get with data
def test_get_item_list_with_data(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    item1 = ItemModel(item_name="Apple", item_price=0.99, store_id=store.store_id)
    item2 = ItemModel(item_name="Banana", item_price=1.49, store_id=store.store_id)
    session.add_all([item1, item2])
    session.commit()

    response = client.get("/item")
    assert response.status_code == 200
    assert len(response.json) == 2


#  test get response keys:
def test_item_list_response_keys(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Water", item_price=2.0, store_id=store.store_id)
    session.add(item)
    session.commit()

    response = client.get("/item")
    assert set(response.json[0].keys()) == {"item_id", "item_name", "item_price", "store", "tags"}


# test post endpind is protected
def test_post_item_requires_auth(client):
    response = client.post("/item", json={})
    assert response.status_code == 401


# test post item
def test_post_item_creates_item(client, session, auth_header):
    store = StoreModel(store_name="Test Store")
    session.add(store)
    session.commit()

    item_data = {
        "item_name": "Phone",
        "item_price": 199.99,
        "store_id": store.store_id
    }
    response = client.post("/item", json=item_data, headers=auth_header)
    assert response.status_code == 201
    assert response.json["item_name"] == "Phone"
    assert response.json["item_price"] == 199.99

# test post item response keys
def test_post_item_response_keys(client, session, auth_header):
    store = StoreModel(store_name="Test Store")
    session.add(store)
    session.commit()

    item_data = {
        "item_name": "Phone",
        "item_price": 199.99,
        "store_id": store.store_id
    }
    response = client.post("/item", json=item_data, headers=auth_header)
    data = response.json
    assert "item_id" in data
    assert "item_name" in data
    assert "item_price" in data
    assert "store" in data
    assert "tags" in data


# test duplicate items in same store are not allowed
def test_post_duplicate_item_in_same_store_raises_409(client, session, auth_header):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    item_data = {
        "item_name": "Monitor",
        "item_price": 199.99,
        "store_id": store.store_id
    }

    # First insertion
    client.post("/item", json=item_data, headers=auth_header)
    # Duplicate insertion
    response = client.post("/item", json=item_data, headers=auth_header)
    assert response.status_code == 409
    assert response.json["message"] == "This item already exists in this store."


# test post store reference to non existent store
def test_post_item_to_non_existing_store_raises_500(client, auth_header):
    item_data = {
        "item_name": "Monitor",
        "item_price": 199.99,
        "store_id": 999
    }
    response = client.post("/item", json=item_data, headers=auth_header)
    print(response.json)
    assert response.status_code == 409
    assert response.json["message"] == "Store referenced does not exist."


# test invalid payload type
def test_post_item_with_invalid_type_returns_422(client, session, auth_header):
    """
    GIVEN invalid data types for item fields (e.g. str instead of float/int)
    WHEN posting to /item
    THEN a 422 error is returned with validation error messages
    """
    store = StoreModel(store_name="Typed Store")
    session.add(store)
    session.commit()

    invalid_item_data = {
        "item_name": 123,
        "item_price": "cheap",
        "store_id": "one"
    }

    response = client.post("/item", json=invalid_item_data, headers=auth_header)

    assert response.status_code == 422
    assert "item_name" in response.json["errors"]["json"]
    assert "item_price" in response.json["errors"]["json"]
    assert "store_id" in response.json["errors"]["json"]


# test invalid payload
def test_post_item_missing_fields_returns_422(client, auth_header):
    response = client.post("/item", json={}, headers=auth_header)
    assert response.status_code == 422
    assert "item_name" in response.json["errors"]["json"]


## /item/<item_id>

# test get by id
def test_get_item_by_id(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Milk", item_price=2.99, store_id=store.store_id)
    session.add(item)
    session.commit()

    response = client.get(f"/item/{item.item_id}")
    assert response.status_code == 200
    assert response.json["item_name"] == "Milk"


# test get by id non-existing item
def test_get_item_by_id_not_found(client):
    response = client.get("/item/999")
    assert response.status_code == 404


# delete item
def test_delete_item_by_id(client, session):
    store = StoreModel(store_name="Deli")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Cheese", item_price=5.0, store_id=store.store_id)
    session.add(item)
    session.commit()

    response = client.delete(f"/item/{item.item_id}")
    assert response.status_code == 200
    assert response.json["message"] == "item deleted"


# test delete non-existing item
def test_delete_item_by_id_not_found(client):
    response = client.delete("/item/12345")
    assert response.status_code == 404


# test update existing item
def test_put_item_updates_existing(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Old", item_price=1.0, store_id=store.store_id)
    session.add(item)
    session.commit()

    updated_data = {
        "item_name": "Updated",
        "item_price": 2.5,
        "store_id": store.store_id
    }

    response = client.put(f"/item/{item.item_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json["item_name"] == "Updated"


# test updates creates with non-existing item
def test_put_item_creates_new_if_not_exist(client, session):
    store = StoreModel(store_name="Upsert Store")
    session.add(store)
    session.commit()

    item_data = {
        "item_name": "New Item",
        "item_price": 10.0,
        "store_id": store.store_id
    }

    response = client.put("/item/100", json=item_data)
    assert response.status_code == 200
    assert response.json["item_name"] == "New Item"
    assert response.json["item_id"] == 100


# test violating unique constraint by update
def test_put_item_raises_409_on_duplicate(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    item1 = ItemModel(item_name="Item A", item_price=1.0, store_id=store.store_id)
    item2 = ItemModel(item_name="Item B", item_price=2.0, store_id=store.store_id)
    session.add_all([item1, item2])
    session.commit()

    response = client.put(f"/item/{item2.item_id}", json={
        "item_name": "Item A",  # Duplicate name in the same store
        "item_price": 3.0,
        "store_id": store.store_id
    })
    print("print")
    print(response.json)
    assert response.status_code == 409
    assert response.json["message"] == "This item already exists in this store."


# test invalid payload when updates non-existing item (cannot create because payload invalid)
def test_put_item_missing_required_fields_on_create_returns_422(client):
    response = client.put("/item/999", json={})
    print(response.json)
    assert response.status_code == 409
    error_message = "This item does not exist neither can be created due to invalid load"
    assert response.json["message"] == error_message


#  test violate foregin key constrint by update
def test_put_item_with_invalid_store_id_raises_409(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Item", item_price=9.99,  store_id=store.store_id)
    session.add(item)
    session.commit()

    response = client.put(f"/item/{item.item_id}", json={
        "store_id": 9999  # Invalid FK
    })

    assert response.status_code == 409
    assert response.json["message"] == "Store referenced does not exist."


# test deleteting store will cascade to all items in that store
def test_delete_store_cascades_to_items(client, session):
    from app.models import ItemModel

    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    item1 = ItemModel(item_name="Soda", item_price=1.99, store_id=store.store_id)
    item2 = ItemModel(item_name="Water", item_price=0.99, store_id=store.store_id)
    session.add_all([item1, item2])
    session.commit()

    response = client.delete(f"/store/{store.store_id}")
    assert response.status_code == 200

    items_remaining = session.query(ItemModel).filter_by(store_id=store.store_id).all()
    assert items_remaining == []
