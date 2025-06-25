from app.models import StoreModel, TagModel, ItemModel


## /store/<store_id>/tag

# test get store tags no data
def test_get_tags_in_store_returns_empty_list(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    response = client.get(f"/store/{store.store_id}/tag")
    assert response.status_code == 200
    assert len(response.json) == 0


# test get store tags with data
def test_get_store_tags_with_data(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    tag1 = TagModel(tag_name="Summer", store_id=store.store_id)
    tag2 = TagModel(tag_name="Winter", store_id=store.store_id)
    session.add_all([tag1, tag2])
    session.commit()

    response = client.get(f"/store/{store.store_id}/tag")

    assert response.status_code == 200
    assert len(response.json) == 2
    tag_names = [tag["tag_name"] for tag in response.json]
    assert "Summer" in tag_names
    assert "Winter" in tag_names


# test 404 if store doesnt exist
def test_get_tags_returns_404_if_store_not_found(client):
    response = client.get("/store/9999/tag")
    assert response.status_code == 404


# test get store response key
def test_get_store_tags_response_keys(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    tag = TagModel(tag_name="Summer", store_id=store.store_id)
    session.add(tag)
    session.commit()

    response = client.get(f"/store/{store.store_id}/tag")

    assert response.status_code == 200
    assert set(response.json[0].keys()) == {"tag_id", "tag_name"}


# test post tag to a store
def test_post_tag_to_store_creates_tag(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    response = client.post(f"/store/{store.store_id}/tag", json={"tag_name": "Summer"})
    assert response.status_code == 201
    assert response.json["tag_name"] == "Summer"
    assert response.json["store"]["store_id"] == store.store_id


# test post tag response keys
def test_post_tag_response_keys(client, session):
    store = StoreModel(store_name="Shoes")
    session.add(store)
    session.commit()

    response = client.post(f"/store/{store.store_id}/tag", json={"tag_name": "Sport"})
    assert response.status_code == 201
    keys = set(response.json.keys())
    assert keys == {"tag_id", "tag_name", "store", "items"}


# test post duplicate tags in the same store not allowed
def test_post_duplicate_tag_in_same_store_raises_400(client, session):
    store = StoreModel(store_name="Books")
    session.add(store)
    session.commit()

    tag = TagModel(tag_name="New", store_id=store.store_id)
    session.add(tag)
    session.commit()

    response = client.post(f"/store/{store.store_id}/tag", json={"tag_name": "New"})
    assert response.status_code == 400
    assert "A tag with that name already exist in that Store." == response.json["message"]


# test post tag to non-existing store
def test_post_tag_to_non_existing_store_returns_404(client):
    response = client.post("/store/9999/tag", json={"tag_name": "Random"})
    assert response.status_code == 409
    assert response.json["message"] == "Store referenced does not exist."


# test invalid payload type
def test_post_tag_with_invalid_type_returns_422(client, session):
    store = StoreModel(store_name="Electronics")
    session.add(store)
    session.commit()

    response = client.post(f"/store/{store.store_id}/tag", json={"tag_name": 123})
    assert response.status_code == 422
    assert "tag_name" in response.json["errors"]["json"]


# test invalid payload
def test_post_tag_with_missing_field_returns_422(client, session):
    store = StoreModel(store_name="Toys")
    session.add(store)
    session.commit()

    response = client.post(f"/store/{store.store_id}/tag", json={})
    assert response.status_code == 422
    assert "tag_name" in response.json["errors"]["json"]


## /tag

# test get with no data
def test_get_tag_list_returns_empty(client):
    response = client.get("/tag")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.json == []


# test get with data
def test_get_tag_list_with_data(client, session):
    store = StoreModel(store_name="General Store")
    session.add(store)
    session.commit()

    tag1 = TagModel(tag_name="Fresh", store_id=store.store_id)
    tag2 = TagModel(tag_name="Organic", store_id=store.store_id)
    session.add_all([tag1, tag2])
    session.commit()

    response = client.get("/tag")
    assert response.status_code == 200
    assert len(response.json) == 2

    tag_names = {tag["tag_name"] for tag in response.json}
    assert tag_names == {"Fresh", "Organic"}


# test get response keys
def test_get_tag_list_response_keys(client, session):
    store = StoreModel(store_name="Shop")
    session.add(store)
    session.commit()

    tag = TagModel(tag_name="Discount", store_id=store.store_id)
    session.add(tag)
    session.commit()

    response = client.get("/tag")
    assert response.status_code == 200
    tag_data = response.json[0]
    assert set(tag_data.keys()) == {"tag_id", "tag_name", "store", "items"}


## /tag/<tag_id>

# test get by id
def test_get_tag_by_id_returns_tag(client, session):
    store = StoreModel(store_name="Test Store")
    session.add(store)
    session.commit()

    tag = TagModel(tag_name="Clearance", store_id=store.store_id)
    session.add(tag)
    session.commit()

    response = client.get(f"/tag/{tag.tag_id}")
    assert response.status_code == 200
    assert response.json["tag_name"] == "Clearance"
    assert "store" in response.json
    # test response keys
    assert set(response.json.keys()) == {"tag_name", "tag_id", "store", "items"}

# test get by id non-existing tag
def test_get_tag_by_id_not_found_returns_404(client):
    response = client.get("/tag/9999")
    assert response.status_code == 404


# test delete tag
def test_delete_tag_without_items_returns_202(client, session):
    store = StoreModel(store_name="Store A")
    session.add(store)
    session.commit()

    tag = TagModel(tag_name="Solo", store_id=store.store_id)
    session.add(tag)
    session.commit()

    response = client.delete(f"/tag/{tag.tag_id}")
    assert response.status_code == 202
    assert response.json["message"] == "Tag deleted."


# test delete non-existing tag
def test_delete_tag_by_id_not_found_returns_404(client):
    response = client.delete("/tag/9999")
    assert response.status_code == 404


# test delete tag assigned to items
def test_delete_tag_with_items_returns_400(client, session):
    store = StoreModel(store_name="Store B")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Item", item_price=10.0, store_id=store.store_id)
    tag = TagModel(tag_name="Attached", store_id=store.store_id)
    session.add_all([item, tag])
    session.commit()

    item.tags.append(tag)
    session.commit()

    response = client.delete(f"/tag/{tag.tag_id}")
    assert response.status_code == 400
    assert "tag is not deleted" in response.json["message"]


## /ietm/<item_id>/tag/<tag_id>

# test link tag to item
def test_link_tag_to_item(client, session):
    store = StoreModel(store_name="Test Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Table", item_price=50.0, store_id=store.store_id)
    tag = TagModel(tag_name="Furniture", store_id=store.store_id)
    session.add_all([item, tag])
    session.commit()

    response = client.post(f"/item/{item.item_id}/tag/{tag.tag_id}")
    assert response.status_code == 201
    assert tag.tag_name in [t["tag_name"] for t in response.json["tags"]]

    # test respose keys
    assert set(response.json.keys()) == {
        "item_id",
        "item_name",
        "item_price",
        "tags",
        "store"
    }


# test link non-existing item or non-esxisting tag
def test_link_non_existing_item_or_tag_returns_404(client, session):
    store = StoreModel(store_name="Test")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Chair", item_price=20.0, store_id=store.store_id)
    tag = TagModel(tag_name="Office", store_id=store.store_id)
    session.add_all([item, tag])
    session.commit()

    assert client.post(f"/item/9999/tag/{tag.tag_id}").status_code == 404
    assert client.post(f"/item/{item.item_id}/tag/9999").status_code == 404


# test link item to a tag in different store (shoild raise 404 or what is related)
def test_link_tag_to_item_from_different_store_fails_or_works(client, session):
    store1 = StoreModel(store_name="Electronics")
    store2 = StoreModel(store_name="Furniture")
    session.add_all([store1, store2])
    session.commit()

    item = ItemModel(item_name="TV", item_price=300.0, store_id=store1.store_id)
    tag = TagModel(tag_name="Home", store_id=store2.store_id)
    session.add_all([item, tag])
    session.commit()

    response = client.post(f"/item/{item.item_id}/tag/{tag.tag_id}")
    assert response.status_code == 400
    assert response.json["message"] == "item and tag must be in the same store."


# test unlink tag from item
def test_unlink_tag_from_item_success(client, session):
    store = StoreModel(store_name="General")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Notebook", item_price=3.0, store_id=store.store_id)
    tag = TagModel(tag_name="Stationery", store_id=store.store_id)
    session.add_all([item, tag])
    session.commit()

    item.tags.append(tag)
    session.commit()

    response = client.delete(f"/item/{item.item_id}/tag/{tag.tag_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Tag was unlinked from item successfully"

    # test response keys
    assert {"message", "tag", "item"} == set(response.json.keys())


# test unlink non-existing item or non-esxisting tag
def test_unlink_non_existing_item_or_tag_returns_404(client, session):
    store = StoreModel(store_name="Unlink Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Marker", item_price=1.5, store_id=store.store_id)
    tag = TagModel(tag_name="Drawing", store_id=store.store_id)
    session.add_all([item, tag])
    session.commit()

    assert client.delete(f"/item/9999/tag/{tag.tag_id}").status_code == 404
    assert client.delete(f"/item/{item.item_id}/tag/9999").status_code == 404


# unlink tag to
def test_unlink_tag_not_associated_with_item_raises_value_error(client, session):
    store = StoreModel(store_name="Store")
    session.add(store)
    session.commit()

    item = ItemModel(item_name="Unlinked Item", item_price=5.0, store_id=store.store_id)
    tag = TagModel(tag_name="Lonely Tag", store_id=store.store_id)
    session.add_all([item, tag])
    session.commit()

    # Do NOT associate tag with item
    response = client.delete(f"/item/{item.item_id}/tag/{tag.tag_id}")
    
    assert response.status_code == 400
    print(response.json)

    assert "Item is not linked to" in response.json["message"]
