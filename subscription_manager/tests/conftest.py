import pytest

from subscription_manager.common import utils
from subscription_manager.controller import Controller
from subscription_manager.dbhelper import DBHelper


@pytest.fixture
def controller(mock_dbhelper: DBHelper) -> Controller:
    """Returns Controller class instance"""
    database = mock_dbhelper
    return Controller(database)


@pytest.fixture
def generated_subscription() -> dict:
    """Returns generated random subscription with correct fields"""
    return utils.subscription_generator()
