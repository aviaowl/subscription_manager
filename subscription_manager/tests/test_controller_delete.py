from unittest.mock import MagicMock

import pytest

from subscription_manager.common.constants import *
from subscription_manager.common.exceptions import SubscriptionException
from subscription_manager.controller import Controller
from subscription_manager.dbhelper import DBHelper


@pytest.fixture
def mock_dbhelper() -> DBHelper:
    """Returns mock for DBHelper"""
    mock = DBHelper
    mock.delete_subscription = MagicMock(return_value=1)
    return mock


def test_delete_subscription(controller: Controller):
    """Test existing subscription deletion"""
    assert controller.delete_subscription("Youtube Music") == 1


@pytest.mark.parametrize(
    "name",
    [
        123,
        4.2,
        ("I am subscription",),
        ["I", "am", "subscription"],
        {"name": "Subscription"},
        None,
    ],
)
def test_delete_subscription_wrong_name(controller: Controller, name):
    """Test that Controller will not delete subscription with subscription name type"""
    with pytest.raises(SubscriptionException) as exc:
        assert controller.delete_subscription(name)
    assert str(exc.value) == WRONG_TYPE_MSG.format(
        expected=str, recieved_type=type(name), field=name
    )


def test_delete_subscription_empty_name(controller: Controller):
    """Test that Controller will not delete subscription with subscription name value"""
    with pytest.raises(SubscriptionException) as exc:
        assert controller.delete_subscription("")
    assert str(exc.value) == EMPTY_FIELD_MSG
