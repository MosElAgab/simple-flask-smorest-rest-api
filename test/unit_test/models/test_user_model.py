from app.models import UserModel


def test_constructor():
    """
    GIVEN a UserModel with required fields
    WHEN an instance is created
    THEN it should store the correct data
    """
    user = UserModel(username="john_doe", password="securepassword123", is_admin=True)
    assert isinstance(user, UserModel)
    assert user.username == "john_doe"
    assert user.password == "securepassword123"
    assert user.is_admin is True


def test_default_is_admin():
    """
    GIVEN a UserModel without explicitly setting is_admin
    WHEN an instance is created
    THEN is_admin should default to False
    """
    user = UserModel(username="jane_doe", password="anotherpassword")
    assert user.is_admin is False
