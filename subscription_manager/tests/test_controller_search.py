from datetime import datetime, date
from unittest.mock import MagicMock

import pytest
from bson import ObjectId

from subscription_manager.controller import Controller
from subscription_manager.dbhelper import DBHelper
from subscription_manager.exceptions import *
from subscription_manager.subscription import Subscription


@pytest.fixture
def mock_dbhelper() -> DBHelper:
    """Returns mock for DBHelper for get_subscription by name from database"""
    mock = DBHelper
    return_dict = {
        "owner": "Mary",
        "name": "Sky Store",
        "frequency": "monthly",
        "start_date": date(2019, 4, 13),
        "price": 12.97,
        "currency": "CNY",
        "comment": "Generation date: 23/06/2020, 10:46:41",
    }
    mock.get_subscription = MagicMock(return_value=return_dict)
    return mock


@pytest.fixture
def mock_dbhelper_not_found(mock_dbhelper: DBHelper) -> DBHelper:
    """Returns mock for DBHelper for get_subscription by name from database with SubsNotFoundException """
    mock = DBHelper
    mock_dbhelper.get_subscription.side_effect = SubsNotFoundException(
        "Subscription with name 'Definitely not exist' was not found"
    )
    return mock


@pytest.fixture
def controller_subs_not_found(mock_dbhelper_not_found: DBHelper) -> Controller:
    """Returns Controller instance with DBHelper mock with SubsNotFoundException"""
    database = mock_dbhelper_not_found
    return Controller(database)


@pytest.fixture
def controller(mock_dbhelper: DBHelper) -> Controller:
    """Returns Controller class instance"""
    database = mock_dbhelper
    return Controller(database)


def test_get_subscription_by_name(controller: Controller):
    """Check correct format of found subscription:
        _id from database is not in the dict
        type(result) == Subscription
        type(start_date) == date, not datetime
        other fields values and types have no changes
    """
    actual_result = controller.get_subscription_by_name("Sky Store")
    expected_result = Subscription(
        owner="Mary",
        name="Sky Store",
        frequency="monthly",
        start_date=date(2019, 4, 13),
        price=12.97,
        currency="CNY",
        comment="Generation date: 23/06/2020, 10:46:41",
    )
    assert actual_result == expected_result


@pytest.mark.parametrize(
    "subscription_name",
    [42, 1.24, ("one", "two"), {"name": "Very important subscription"}, None],
)
def test_get_subscription_by_wrong_name_type(
    controller: Controller, subscription_name: str
):
    """Check search with subscription_name wrong type"""
    with pytest.raises(SubscriptionException) as exc:
        controller.get_subscription_by_name(subscription_name)
    expected_err_msg = (
        f"Found wrong field 'subscription_name' type, expected: <str>, "
        f"received: ({type(subscription_name)}, {subscription_name})"
    )
    assert str(exc.value) == expected_err_msg


def test_get_subscription_by_empty_name(controller: Controller):
    """Check correct behaviour in case of empty subscription_name"""
    with pytest.raises(InvalidValueException) as exc:
        controller.get_subscription_by_name("")
    expected_err_msg = "Subscription name length should be more than one"
    assert str(exc.value) == expected_err_msg


def test_get_not_exist_subscription(controller_subs_not_found: Controller):
    """Check correct behaviour in case of nonexistent subscription_name"""
    with pytest.raises(SubsNotFoundException) as exc:
        assert controller_subs_not_found.get_subscription_by_name(
            "Definitely not exist"
        )
    assert (
        str(exc.value) == "Subscription with name 'Definitely not exist' was not found"
    )
