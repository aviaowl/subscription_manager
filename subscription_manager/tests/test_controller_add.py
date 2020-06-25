import pytest
from subscription_manager.exceptions import SubscriptionException
import subscription_manager.utils as utils
from dateutil.relativedelta import relativedelta
from subscription_manager.controller import Controller
from subscription_manager.dbhelper import DBHelper
from bson.objectid import ObjectId
from unittest.mock import MagicMock
from datetime import datetime


@pytest.fixture
def subscription_dict() -> dict:
    """Returns generated random subscription with correct fields"""
    return utils.subscription_generator()


@pytest.fixture
def mock_dbhelper() -> DBHelper:
    """Returns mock for DBHelper to avoid writing to production database"""
    mock = DBHelper
    mock.add_subscription = MagicMock(return_value=ObjectId("5ef2081b329cba6d5b03b6ff"))
    return mock


@pytest.fixture
def controller(mock_dbhelper: DBHelper) -> Controller:
    """Returns Controller class instance"""
    database = mock_dbhelper
    return Controller(database)


@pytest.mark.parametrize(
    "subscription_dict", [utils.subscription_generator() for _ in range(5)]
)
def test_add_subscription(subscription_dict: dict, controller: Controller):
    """Check successful subscription addition with correct parameters"""
    result = controller.add_subscription(subscription_dict)
    assert type(result) == ObjectId


@pytest.mark.parametrize(
    "paramNone",
    ["owner", "name", "frequency", "start_date", "price", "currency", "comment"],
)
def test_add_subscription_with_none_fields(
    controller: Controller, subscription_dict: dict, paramNone: str
):
    """Check subscribe addition with one of the field equals None"""
    sub_dict = subscription_dict.copy()
    sub_dict[paramNone] = None
    with pytest.raises(SubscriptionException) as exc:
        assert controller.add_subscription(sub_dict)
    # Receive expected type from valid subscription instance by field name
    expected_exc_msg = (
        f"Found wrong field '{paramNone}' type, "
        f"expected:{type(subscription_dict[paramNone])}, received:(<class "
        "'NoneType'>, None)"
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
    subscription_dict: dict, controller: Controller, field: str, value
):
    """Check that Controller will not add subscription with wrong field types"""
    sub_dict = subscription_dict.copy()
    sub_dict[field] = value
    with pytest.raises(SubscriptionException) as exc:
        assert controller.add_subscription(sub_dict)
    # Receive expected type from valid subscription instance by field name
    expected_exc_msg = (
        f"Found wrong field '{field}' type, "
        f"expected:{type(subscription_dict[field])}, received:({type(value)}, {value})"
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
    subscription_dict: dict, controller: Controller, field: str, value
):
    """Check that Controller will not add subscription with wrong field values"""
    sub_dict = subscription_dict.copy()
    sub_dict[field] = value
    with pytest.raises(SubscriptionException):
        assert controller.add_subscription(sub_dict)
