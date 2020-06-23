import pytest
import subscription_manager.utils as utils
from dateutil.relativedelta import relativedelta
from subscription_manager.controller import Controller
from subscription_manager.subscription import Subscription
from subscription_manager.dbhelper import DBHelper
from bson.objectid import ObjectId
from unittest.mock import MagicMock
from subscription_manager.utils import InvalidSubsFieldException, MissingFieldsException
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
def controller(mock_dbhelper) -> Controller:
    """Returns Controller class instance"""
    database = mock_dbhelper
    return Controller(database)


@pytest.fixture
def subscription(subs_dict: dict) -> Subscription:
    """Returns Subscription class instance"""
    return Subscription(**subs_dict)


@pytest.mark.parametrize("subscription_dict", [utils.subscription_generator() for _ in range(5)])
def test_add_subscription(subscription_dict, controller):
    """Check successful subscription addition with correct parameters"""
    result = controller.add_subscription(subscription_dict)
    assert type(result) == ObjectId


@pytest.mark.parametrize("paramNone", ['owner', 'name', 'frequency', 'start_date', 'price', 'currency', 'comment'])
def test_add_subscription_with_none_fields(controller, subscription_dict, paramNone):
    """Check subscribe addition with one of the field equals None"""
    sub_dict = subscription_dict
    sub_dict[paramNone] = None
    with pytest.raises(InvalidSubsFieldException):
        assert controller.add_subscription(sub_dict)


def test_add_subscription_empty(controller):
    """Check that Controller will not add empty subscription"""
    with pytest.raises(MissingFieldsException):
        assert controller.add_subscription({})


@pytest.mark.parametrize("field, value, expected_error",
                         [('owner', 123, InvalidSubsFieldException),
                          ('name', 4.56, InvalidSubsFieldException),
                          ('frequency', 31, InvalidSubsFieldException),
                          ('start_date', 1012020, InvalidSubsFieldException),
                          ('price', 'two', InvalidSubsFieldException),
                          ('currency', 1.01, InvalidSubsFieldException),
                          ('comment', int, InvalidSubsFieldException)])
def test_add_subscription_wrong_types(subscription_dict, controller, field, value, expected_error):
    """Check that Controller will not add subscription with wrong field types"""
    sub_dict = subscription_dict
    sub_dict[field] = value
    with pytest.raises(expected_error):
        assert controller.add_subscription(sub_dict)


@pytest.mark.parametrize("field, value", [('start_date', datetime.today() + relativedelta(days=+1)),
                                          ('frequency', 'wrong'),
                                          ('currency', 'dollar'),
                                          ('currency', 'CAD')])
def test_add_subscription_wrong_values(subscription_dict, controller, field, value):
    """Check that Controller will not add subscription with wrong field values"""
    sub_dict = subscription_dict
    sub_dict[field] = value
    with pytest.raises(InvalidSubsFieldException):
        assert controller.add_subscription(sub_dict)
