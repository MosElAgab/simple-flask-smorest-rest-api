import pytest
from app import create_app


def test_invalid_config_name_raises_value_error():
    with pytest.raises(ValueError):
        create_app("invalid_config_name")

