
import pytest
from app import create_app
from app.config import config_mapping


def test_invalid_config_name_raises_value_error():
    """
    Given create_app function
    When invlaid config_name is give
    Then ensure it raises value error
    """
    with pytest.raises(ValueError):
        create_app("invalid_config_name")


def test_create_app_loads_default_configs():
    app = create_app()
    assert app.config["PROPOGATE_EXCEPTIONS"] is True
    assert len(app.config["JWT_SECRET_KEY"]) == 39
    assert app.config["DEBUG"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] ==  "sqlite:///dev-data.db"
    assert app.config["TESTING"] is False


@pytest.mark.parametrize("config_name", ["development", "testing", "production"])
def test_create_app_loads_configs_using_config_name(config_name):
    create_app(config_name)
    cfg = config_mapping[config_name]
    app = create_app(config_name=config_name)
    print(config_name)
    assert app.config["TESTING"] is getattr(cfg, "TESTING", False)
    assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False
