from datetime import datetime
from unittest.mock import MagicMock

import pytest
from bson.objectid import ObjectId
from dateutil.relativedelta import relativedelta

import subscription_manager.common.utils as utils
from subscription_manager.common.constants import *
from subscription_manager.common.exceptions import SubscriptionException
from subscription_manager.controller import Controller
from subscription_manager.dbhelper import DBHelper


@pytest.fixture
def mock_dbhelper() -> DBHelper:
    """Returns mock for DBHelper to avoid writing to production database"""
    mock = DBHelper
    mock.add_subscription = MagicMock(return_value=ObjectId("5ef2081b329cba6d5b03b6ff"))
    return mock


@pytest.mark.parametrize(
    "generated_subscription", [utils.subscription_generator() for _ in range(5)]
)
def test_add_subscription(generated_subscription: dict, controller: Controller):
    """Check successful subscription addition with correct parameters"""
    result = controller.add_subscription(generated_subscription)
    assert type(result) == ObjectId


@pytest.mark.parametrize(
    "paramNone",
    ["owner", "name", "frequency", "start_date", "price", "currency", "comment"],
)
def test_add_subscription_with_none_fields(
    controller: Controller, generated_subscription: dict, paramNone: str
):
    """Check subscribe addition with one of the field equals None"""
    sub_dict = generated_subscription.copy()
    sub_dict[paramNone] = None
    with pytest.raises(SubscriptionException) as exc:
        assert controller.add_subscription(sub_dict)
    # Receive expected type from valid subscription instance by field name
    expected_exc_msg = WRONG_TYPE_MSG.format(
        expected=type(generated_subscription[paramNone]),
        recieved_type=type(None),
        field=None,
    )
    assert str(exc.value) == expected_exc_msg


def test_add_subscription_empty(controller: Controller):
    """Check that Controller will not add empty subscription"""
    with pytest.raises(SubscriptionException):
        assert controller.add_subscription({})


@pytest.mark.parametrize(
    "field, value",
    [
        ("owner", 123),
        ("name", 4.56),
        ("frequency", 31),
        ("start_date", 1012020),
        ("price", 1),
        ("currency", 1.01),
        ("comment", 42),
    ],
)
def test_add_subscription_wrong_types(
    generated_subscription: dict, controller: Controller, field: str, value
):
    """Check that Controller will not add subscription with wrong field types"""
    sub_dict = generated_subscription.copy()
    sub_dict[field] = value
    with pytest.raises(SubscriptionException) as exc:
        assert controller.add_subscription(sub_dict)
    # Receive expected type from valid subscription instance by field name
    expected_exc_msg = WRONG_TYPE_MSG.format(
        expected=type(generated_subscription[field]),
        recieved_type=type(value),
        field=value,
    )
    assert str(exc.value) == expected_exc_msg


@pytest.mark.parametrize(
    "field, value",
    [
        ("start_date", datetime.today() + relativedelta(days=+1)),
        ("frequency", "wrong"),
        ("currency", "dollar"),
        ("currency", "CAD"),
    ],
)
def test_add_subscription_wrong_values(
    generated_subscription: dict, controller: Controller, field: str, value
):
    """Check that Controller will not add subscription with wrong field values"""
    sub_dict = generated_subscription.copy()
    sub_dict[field] = value
    with pytest.raises(SubscriptionException):
        assert controller.add_subscription(sub_dict)
