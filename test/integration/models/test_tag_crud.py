import pytest
from sqlalchemy.exc import IntegrityError

from app.models import TagModel, StoreModel


def test_tag_crud_operations(session):
    """
    GIVEN a TagModel instance
    WHEN it is created, queried, updated, and deleted
    THEN the operations should behave as expected
    """
    from app.models import StoreModel, TagModel

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


def test_tag_requires_store(session):
    """
    GIVEN an ItemModel with no valid store_id
    WHEN it's added to the session
    THEN an IntegrityError should be raised
    """
    tag = TagModel(tag_name="Electronics", store_id=99999)# Invalid FK
    session.add(tag)
    with pytest.raises(IntegrityError):
        session.commit()


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


#TODO: test teg item relationship (invloves many-to-many)
