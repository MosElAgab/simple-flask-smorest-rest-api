
import pytest
from app import create_app


def test_invalid_config_name_raises_value_error():
    """
    Given create_app function
    When invlaid config_name is give
    Then ensure it raises value error
    """
    with pytest.raises(ValueError):
        create_app("invalid_config_name")

