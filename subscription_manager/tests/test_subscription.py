import pytest
import datetime
from subscription_manager import Subscription


@pytest.fixture
def subscription() -> Subscription.Subscription:
    """Returns Subscription class instance"""
    subscription_dict = {'owner': 'Lena',
                         'name': 'Amazon Prime',
                         'frequency': '1 month',
                         'start_date': datetime.datetime(2020, 6, 18, 11, 38, 56, 372274),
                         'price': 8.99,
                         'currency': 'GBP',
                         'comment': 'Prime membership for faster delivery'}

    return Subscription.Subscription(**subscription_dict)


def test_subscription_representation(subscription):
    """Test subscription representation __repr__"""
    expected = "Subscription(owner='Lena', " \
               "name='Amazon Prime', " \
               "frequency='1 month', " \
               "start_date=datetime.datetime(2020, 6, 18, 11, 38, 56, 372274), " \
               "price=8.99, " \
               "currency='GBP', " \
               "comment='Prime membership for faster delivery')"
    assert subscription.__repr__() == expected


def test_subscription_str(subscription):
    """Test subscription string representation __str__"""
    expected = "(Lena, " \
               "Amazon Prime, " \
               "1 month, " \
               "2020-06-18 11:38:56.372274, " \
               "8.99, " \
               "GBP, " \
               "Prime membership for faster delivery)"
    assert str(subscription) == expected
