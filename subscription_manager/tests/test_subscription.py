import pytest
from subscription_manager.subscription import Subscription, WrongFrequency
from datetime import datetime
from dateutil.relativedelta import relativedelta

today = datetime.today().date()


@pytest.fixture
def subscription() -> Subscription:
    """Returns Subscription class instance"""
    return Subscription(owner='Lena',
                        name='Amazon Prime',
                        frequency='1 month',
                        start_date=datetime(2020, 6, 18, 11, 38, 56, 372274),
                        price=8.99,
                        currency='GBP',
                        comment='Prime membership for faster delivery')


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


@pytest.mark.parametrize("start_date, frequency, expected",
                         [(datetime(2020, 1, 1), 'daily', today),
                          (today - relativedelta(weeks=1, days=1), 'weekly', today + relativedelta(weeks=1, days=-1)),
                          (today - relativedelta(months=1, days=1), 'monthly', today + relativedelta(months=1, days=-1)),
                          (today - relativedelta(years=1, days=1), 'yearly', today + relativedelta(years=1, days=-1))])
def test_get_next_payment_date(subscription, start_date, frequency, expected):
    """Check that get next payment date works correctly"""
    assert subscription.get_next_payment_date(start_date, frequency) == expected


def test_get_next_payment_date_wrong_frequency(subscription):
    """Test that error occurs in case of calling get next payment date with wrong frequency"""
    with pytest.raises(WrongFrequency) as err:
        subscription.get_next_payment_date(today, 'blahblah')
    assert str(err.value) == 'Unable to parse frequency: expected format examples: daily, weekly, monthly, yearly'
