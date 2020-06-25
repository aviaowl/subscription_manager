import pytest
import subscription_manager.utils as utils
from subscription_manager.subscription import Subscription
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

today = date.today()


@pytest.fixture
def subscription() -> Subscription:
    """Return Subscription class instance"""
    return Subscription(owner='Lena',
                        name='Amazon Prime',
                        frequency='monthly',
                        start_date=date(2020, 6, 18),
                        price=8.99,
                        currency='GBP',
                        comment='Prime membership for faster delivery')


@pytest.fixture
def generated_subscription() -> dict:
    """Return generated subscription with correct fields"""
    return utils.subscription_generator()


def test_subscription_representation(subscription):
    """Test subscription representation __repr__"""
    expected = "Subscription(owner='Lena', " \
               "name='Amazon Prime', " \
               "frequency='monthly', " \
               "start_date=datetime.date(2020, 6, 18), " \
               "price=8.99, " \
               "currency='GBP', " \
               "comment='Prime membership for faster delivery')"
    assert subscription.__repr__() == expected


def test_subscription_str(subscription):
    """Test subscription string representation __str__"""
    expected = '(Lena, ' \
               'Amazon Prime, ' \
               'monthly, ' \
               '2020-06-18, ' \
               '8.99, ' \
               'GBP, ' \
               'Prime membership for faster delivery)'
    assert str(subscription) == expected


@pytest.mark.parametrize("start_date, frequency, expected",
                         [(date(2020, 1, 1), 'daily', today),
                          (today - relativedelta(weeks=1, days=1), 'weekly', today + relativedelta(weeks=1, days=-1)),
                          (today - relativedelta(months=1, days=1), 'monthly',
                           today + relativedelta(months=1, days=-1)),
                          (today - relativedelta(years=1, days=1), 'yearly', today + relativedelta(years=1, days=-1))])
def test_get_next_payment_date(generated_subscription, start_date, frequency, expected):
    """Check that get next payment date works correctly"""
    test_subscription = Subscription(owner=generated_subscription['owner'],
                                     name=generated_subscription['name'],
                                     frequency=frequency,
                                     start_date=start_date,
                                     price=generated_subscription['price'],
                                     currency=generated_subscription['currency'],
                                     comment=generated_subscription['comment'])
    assert test_subscription.get_next_payment_date() == expected
