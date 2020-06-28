from dataclasses import asdict
from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from subscription_manager.common import utils
from subscription_manager.common.exceptions import SubscriptionException
from subscription_manager.controller import Controller
from subscription_manager.dbhelper import DBHelper
from subscription_manager.subscription import Subscription


@pytest.fixture
def mock_dbhelper() -> DBHelper:
    """Returns mock for DBHelper"""
    mock = DBHelper
    mock.update_subscription = MagicMock(return_value=1)
    return mock


@pytest.fixture
def get_subscription() -> Subscription:
    """Returns Subscription object"""
    return Subscription(
        owner="Mary",
        name="Sky Store",
        frequency="monthly",
        start_date=date(2019, 4, 13),
        price=12.97,
        currency="CNY",
        comment="Generation date: 23/06/2020, 10:46:41",
    )


@pytest.mark.parametrize(
    "changes",
    [
        dict(owner="Geralt", name="Lutik Music"),
        dict(frequency="daily", start_date=date(2019, 12, 20)),
        dict(frequency="daily", price=1.00),
        dict(currency="USD", comment="Very funny songs"),
    ],
)
def test_edit_subscription(
    controller: Controller, get_subscription: Subscription, changes: dict
):
    """Check that function returns correct Subscription object for update.
       Examples:
        taken dict: {"a": 1, "b": 2, "c":3}
        changes: {"b": 4, "c": 5}
        returns: {"a":1, "b": 4, "c": 5}
    """
    # Fix Subscription before changes
    before = get_subscription
    before_dict = asdict(get_subscription)

    # Fix Subscription after changes
    after: Subscription = utils.validate_subscription_changes(before, changes)
    after_dict = asdict(after)

    # Find the list of keys that should not change
    unchanged_keys = set(before_dict.keys()) - set(changes.keys())

    # Check that the fields that should not have changed have not changed.
    assert all(before_dict[x] == after_dict[x] for x in unchanged_keys)
    # Check that the fields that were supposed to change have changed.
    assert all(after_dict[x] == changes[x] for x in changes.keys())


@pytest.mark.parametrize(
    "field, value",
    [
        ("owner", 123),
        ("name", ("name",)),
        ("frequency", "not very often"),
        ("start_date", datetime(2020, 1, 1, 0, 0, 0)),
        ("price", 4),
        ("currency", "coin for your Witcher"),
        ("comment", {"oh valley of plenty": "o-o-o-h"}),
    ],
)
def test_edit_subscription_wrong_field_types(
    controller: Controller, get_subscription: Subscription, field, value
):
    subscription = get_subscription
    changes = {field: value}
    with pytest.raises(SubscriptionException):
        assert utils.validate_subscription_changes(subscription, changes)
