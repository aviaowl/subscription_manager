import pytest
import datetime
from subscription_manager.controller import Controller
from subscription_manager.subscription import Subscription
from subscription_manager.dbhelper import DBHelper
import subscription_manager.utils as utils

_DB_URL = '127.0.0.1:8080'
_DB_USER = 'user'
_DB_PASSWORD = 'password'
_DB_COLLECTION = 'collection'


@pytest.fixture
def subscription_dict():
    return {'owner': 'Lena',
            'name': 'Amazon Prime',
            'frequency': '1 month',
            'start_date': datetime.datetime(2020, 6, 18, 11, 38, 56, 372274),
            'price': 8.99,
            'currency': 'GBP',
            'comment': 'Prime membership for faster delivery'}


@pytest.fixture
def controller() -> Controller:
    """Returns Controller class instance"""
    database = DBHelper(_DB_URL, dict(user=_DB_USER, password=_DB_PASSWORD), _DB_COLLECTION)
    return Controller(database)


@pytest.fixture
def subscription(subs_dict: dict) -> Subscription:
    """Returns Subscription class instance"""
    return Subscription(**subs_dict)


@pytest.mark.parametrize("subscription_dict", [utils.subscription_generator(),
                                               utils.subscription_generator(),
                                               utils.subscription_generator()])
def test_add_subscription(subscription_dict, controller):
    """Check successful subscription addition with correct parameters"""
    assert type(controller.add_subscription(subscription_dict)) == int


@pytest.mark.parametrize("paramNone, expected_error",
                         [('owner', None),
                          ('name', ValueError),
                          ('frequency', ValueError),
                          ('start_date', ValueError),
                          ('price', ValueError),
                          ('currency', ValueError),
                          ('comment', None)])
def test_add_subscription_with_none_fields(controller, subscription_dict, expected_error, paramNone):
    """Check subscribe addition with one of the field equals None"""
    subscription_dict[paramNone] = None
    if expected_error:
        with pytest.raises(expected_error):
            assert controller.add_subscription(subscription_dict)
    else:
        assert type(controller.add_subscription(subscription_dict)) == int


def test_add_subscription_empty(controller):
    """Check that Controller will not add empty subscription"""
    with pytest.raises(ValueError):
        assert controller.add_subscription({})


@pytest.mark.parametrize("field, value, expected_error",
                         [('owner', 123, ValueError),
                          ('name', 4.56, ValueError),
                          ('frequency', 31, ValueError),
                          ('start_date', 1012020, ValueError),
                          ('price', 'two', ValueError),
                          ('currency', 1.01, ValueError),
                          ('comment', int, None)])
def test_add_subscription_wrong_types(controller, field, value, expected_error):  # field, wrong_type, expected_error
    """Check that Controller will not add subscription with wrong field types"""
    subscription_dict[field] = int(subscription_dict[field])
    if expected_error:
        with pytest.raises(expected_error):
            assert controller.add_subscription(subscription_dict)
