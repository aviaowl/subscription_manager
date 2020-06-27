from datetime import date
from unittest.mock import MagicMock

import pytest

from subscription_manager.controller import Controller
from subscription_manager.dbhelper import DBHelper
from subscription_manager.exceptions import SubscriptionException
from subscription_manager.subscription import Subscription


@pytest.fixture
def subscriptions_db_list():
    return [
        {
            "comment": "Generation date: 23/06/2020, 10:46:11",
            "currency": "USD",
            "frequency": "daily",
            "name": "Youtube Music",
            "owner": "Kevin",
            "price": 8.3,
            "start_date": date(2019, 5, 11),
        },
        {
            "comment": "Generation date: 23/06/2020, 10:46:41",
            "currency": "CNY",
            "frequency": "monthly",
            "name": "Sky Store",
            "owner": "Mary",
            "price": 12.97,
            "start_date": date(2019, 4, 13),
        },
        {
            "comment": "Generation date: 23/06/2020, 10:47:36",
            "currency": "EUR",
            "frequency": "weekly",
            "name": "Spotify",
            "owner": "Robin",
            "price": 30.23,
            "start_date": date(2019, 10, 19),
        },
    ]


subscriptions_obj_list = [
    Subscription(
        owner="Kevin",
        name="Youtube Music",
        frequency="daily",
        start_date=date(2019, 5, 11),
        price=8.3,
        currency="USD",
        comment="Generation date: 23/06/2020, 10:46:11",
    ),
    Subscription(
        owner="Mary",
        name="Sky Store",
        frequency="monthly",
        start_date=date(2019, 4, 13),
        price=12.97,
        currency="CNY",
        comment="Generation date: 23/06/2020, 10:46:41",
    ),
    Subscription(
        owner="Robin",
        name="Spotify",
        frequency="weekly",
        start_date=date(2019, 10, 19),
        price=30.23,
        currency="EUR",
        comment="Generation date: 23/06/2020, 10:47:36",
    ),
]


@pytest.fixture
def mock_dbhelper(subscriptions_db_list) -> DBHelper:
    """Returns mock for DBHelper for get_subscription by name from database"""
    mock = DBHelper
    mock.get_all_subscriptions = MagicMock(return_value=subscriptions_db_list)
    return mock


@pytest.fixture
def controller(mock_dbhelper: DBHelper) -> Controller:
    """Returns Controller class instance"""
    database = mock_dbhelper
    return Controller(database)


@pytest.mark.parametrize("owner", ["Lena", None])
def test_get_all_subscriptions(controller: Controller, owner: str):
    """Check that Controller returned correct list of Subscription objects:
        - No _id specified in each subscription
        - type is not dict, but Subscription
        - start_date field type is not datetime, but date
    """
    result = controller.get_subscriptions_list(owner)
    assert result == subscriptions_obj_list


@pytest.mark.parametrize("owner", [123, ("Lena", "Artur"), {"owner": "Lena"}])
def test_get_all_subscriptions_wrong_type(controller: Controller, owner):
    """Check that Controller raises exception in case of invalid owner field type"""
    with pytest.raises(SubscriptionException) as exc:
        result = controller.get_subscriptions_list(owner)
        assert result == subscriptions_obj_list
    expected_exc_msg = f"Found wrong owner name's type, expected: <str>, received: {type(owner), owner}"
    assert expected_exc_msg == str(exc.value)


def test_get_all_subscriptions_wrong_value(controller: Controller):
    """Check that Controller raises exception in case of empty owner field"""
    with pytest.raises(SubscriptionException) as exc:
        result = controller.get_subscriptions_list("")
        assert result == subscriptions_obj_list
    expected_exc_msg = "Owner field length should be more than one"
    assert expected_exc_msg == str(exc.value)


def test_get_next_payment_date(controller: Controller):
    """Check that client can get next_payment_date attribute for subscriptions in subscription list"""
    subscriptions_list = controller.get_subscriptions_list()
    assert type(subscriptions_list[0]) == Subscription
    for subs in subscriptions_list:
        assert type(subs.next_payment_date) is date
