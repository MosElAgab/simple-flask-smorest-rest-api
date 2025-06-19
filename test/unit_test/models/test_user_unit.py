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
    assert isinstance(user.username, str)
    assert user.password == "securepassword123"
    assert isinstance(user.password, str)
    assert user.is_admin is True
    assert isinstance(user.is_admin, bool)
