import pytest
from sqlalchemy.exc import IntegrityError

from app.models import UserModel

# test crud operation (create, retieve, update and delete)
def test_user_crud_operations(session):
    user = UserModel(username="user", password="hardpassword", is_admin=True)
    session.add(user)
    session.commit()

    # create
    user_id = user.user_id
    assert user_id is not None

    # Retrieve
    retrieved = session.query(UserModel).filter_by(user_id=user_id).first()
    assert retrieved.username == "user"

    # Update
    retrieved.username = "updated_user"
    session.commit()
    assert session.query(UserModel).filter_by(user_id=user_id).first().username == "updated_user"

    # Delete
    session.delete(retrieved)
    session.commit()
    assert session.query(UserModel).filter_by(user_id=user_id).first() is None


# test for username uniqueness
def test_username_uniqueness_constraint(session):
    user1 = UserModel(username="unique_user", password="123456")
    user2 = UserModel(username="unique_user", password="123456")

    session.add(user1)
    session.commit()

    session.add(user2)
    with pytest.raises(IntegrityError):
        session.commit()


# test for field nullability
@pytest.mark.parametrize("user_data", [
    {"username": None, "password": "abcefg"},   # Null username
    {"password": "abcefg"},   # Missing username
    {"username": "abc", "password": None},    # Null password
    {"username": "abc"}    # Missing password
])
def test_user_required_fields(session, user_data):
    user = UserModel(**user_data)
    session.add(user)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


# test for default values
def test_user_is_admin_defaults_to_false(session):
    user = UserModel(username="jane_doe", password="123456")
    session.add(user)
    session.commit()

    retrieved = session.query(UserModel).filter_by(username="jane_doe").first()
    assert retrieved.is_admin is False
