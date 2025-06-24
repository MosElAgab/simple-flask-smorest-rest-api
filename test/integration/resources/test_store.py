import pytest

from app.models import StoreModel, ItemModel, TagModel


## /store

# test get with no data
def test_get_store_list_retruns_empty_list(client):
    """
    GIVEN no stores in DB
    WHEN GET /store is called
    THEN it returns an empty list
    """
    response = client.get("/store")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 0


# test get with data
def test_get_store_list_with_data(client, session):
    store1 = StoreModel(store_name="Store 1")
    store2 = StoreModel(store_name="Store 2")
    session.add_all([store1, store2])
    session.commit()

    response = client.get("/store")
    assert response.status_code == 200
    assert len(response.json) == 2
    for store in response.json:
        assert "store_id" in store


#  test get response keys:
def test_store_get_returns_expected_keys(client, session):
    store = StoreModel(store_name="InspectMe")
    session.add(store)
    session.commit()

    response = client.get("/store")
    assert response.status_code == 200
    assert set(response.json[0].keys()) == {"store_id", "store_name"}


# test for nested items and tags
def test_get_store_by_id_includes_nested_items_and_tags(client, session):

    # Arrange: create store
    store = StoreModel(store_name="Store with Nested")
    session.add(store)
    session.commit()

    # Arrange: create items and tags for the store
    item1 = ItemModel(item_name="Bread", item_price=1.5, store_id=store.store_id)
    item2 = ItemModel(item_name="Butter", item_price=2.0, store_id=store.store_id)
    tag1 = TagModel(tag_name="Grocery", store_id=store.store_id)
    tag2 = TagModel(tag_name="Dairy", store_id=store.store_id)

    session.add_all([item1, item2, tag1, tag2])
    session.commit()

    # Associate tags with items
    item1.tags.append(tag1)
    item2.tags.append(tag2)
    session.commit()

    # Act: GET /store/<id>
    response = client.get(f"/store/{store.store_id}")
    assert response.status_code == 200

    data = response.json

    # Assert store fields
    assert data["store_name"] == "Store with Nested"
    assert data["store_id"] == store.store_id

    # Assert nested items
    assert len(data["items"]) == 2
    item_names = {item["item_name"] for item in data["items"]}
    assert item_names == {"Bread", "Butter"}

    # Assert nested tags
    assert len(data["tags"]) == 2
    tag_names = {tag["tag_name"] for tag in data["tags"]}
    assert tag_names == {"Grocery", "Dairy"}


# test post endpind is protected
def test_post_store_requires_auth(client):
    response = client.post("/store", json={"store_name": "Store"})
    assert response.status_code == 401
    print(response.json)
    assert response.json["description"] == "Request does not contain an access token."
    assert response.json["error"] == "authorization_required"


# test post store
def test_post_store_creates_store(client, auth_header):
    store_data = {"store_name": "New Store"}
    response = client.post("/store", json=store_data, headers=auth_header)
    print(response.json)
    assert response.status_code == 201
    assert response.json["store_name"] == "New Store"
    assert response.json["store_id"] is not None


# test post store respnse keys
def test_post_store_response_keys(client, auth_header):
    response = client.post("/store", json={"store_name": "SchemaTest"}, headers=auth_header)
    data = response.json
    assert "store_id" in data
    assert "store_name" in data
    assert set(data.keys()) == {"store_id", "store_name"}


# test post duplicate store
def test_post_duplicate_store_raises_409(client, auth_header):
    client.post("/store", json={"store_name": "Duplicate"}, headers=auth_header)
    response = client.post("/store", json={"store_name": "Duplicate"}, headers=auth_header)

    assert response.status_code == 409
    assert response.json["message"] == "A store with this name already exists."


# test invalid payload
def test_post_store_with_missing_field_returns_422(client, auth_header):
    response = client.post("/store", json={}, headers=auth_header)
    assert response.status_code == 422
    assert "store_name" in response.json["errors"]["json"]


# test invalid payload type
def test_post_store_with_invalid_type_returns_422(client, auth_header):
    response = client.post("/store", json={"store_name": 123}, headers=auth_header)
    assert response.status_code == 422
    assert "store_name" in response.json["errors"]["json"]


## /store/<store_id>

# test get by id
def test_get_store_by_id_returns_store(client, session):
    store = StoreModel(store_name="Target Store")
    session.add(store)
    session.commit()

    response = client.get(f"/store/{store.store_id}")
    assert response.status_code == 200
    assert response.json["store_id"] == store.store_id
    assert response.json["store_name"] == "Target Store"


# test get by id non-existing store
def test_get_store_by_id_not_found(client):
    response = client.get("/store/999")
    assert response.status_code == 404


# delete store
def test_delete_store_by_id(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    response = client.delete(f"/store/{store.store_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Store deleted"

    get_response = client.get(f"/store/{store.store_id}")
    assert get_response.status_code == 404


# test delete non-existing store
def test_delete_store_not_found_returns_404(client):
    response = client.delete("/store/999")
    assert response.status_code == 404


# test update existing store
def test_put_store_updates_existing_store(client, session):
    store = StoreModel(store_name="Old name")
    session.add(store)
    session.commit()

    response = client.put(
        f"/store/{store.store_id}",
        json={"store_name": "New name"}
    )
    assert response.status_code == 200
    assert response.json["store_name"] == "New name"
    assert response.json["store_id"] == store.store_id


# test updates creates with non-existing store
def test_put_store_creates_if_not_exists(client):
    response = client.put(
        "/store/100",
        json={"store_name": "created"}
    )
    assert response.status_code == 200
    assert response.json["store_name"] == "created"
    assert response.json["store_id"] == 100


# test violating unique constraint by update
def test_put_store_raises_500_on_integrity_error(client, session):
    session.add(StoreModel(store_name="Existing"))
    session.commit()

    session.add(StoreModel(store_id=50, store_name="ToBeUpdated"))
    session.commit()

    response = client.put("/store/50", json={"store_name": "Existing"})
    assert response.status_code == 409
    assert "A store with this name already exists." in response.json["message"]
