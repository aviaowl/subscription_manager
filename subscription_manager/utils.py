from typing import List
from random import choice, uniform

from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, WEEKLY, MONTHLY, YEARLY, rrule
from datetime import datetime
from pprint import pprint


def validate_subscription(subscription: dict) -> bool:
    """
    Take subscription and validate its every field
    Args:
        subscription (dict): subscription to validate
    Returns:
        True: in case of valid subscription
        False: in case of invalid subscription
    Raises:
        WrongCurrencyError: If input currency is not supported
    """
    pass


def _get_currencies_list() -> List[str]:
    """
    Return list of supported currencies.
    Returns:
        currencies (list): list of supported currencies
    """
    return 'USD', 'GBP', 'EUR', 'RUB', 'CNY'


def subscription_generator() -> dict:
    """
    Generate subscription with correct fields.
    Returns:
        subscription (dict): generated subscription
    """
    names = ['Mary', 'Eva', 'Nancy', 'Ann', 'Kevin', 'John', 'Ben', 'Robin']
    currencies = _get_currencies_list()
    subscription_names = ['Google music', 'Spotify', 'Apple Music', 'Youtube Music', 'Coursera', 'Pluralsight',
                          'Amazon Prime', 'Netflix', 'Sky Store', 'Pet insurance', 'Mobile payment']
    frequencies = ['daily', 'weekly', 'monthly', 'yearly']
    start_dates = list(
        rrule(WEEKLY, dtstart=datetime(2018, 9, 1).date(), until=datetime.today().date()))
    return dict(owner=choice(names),
                name=choice(subscription_names),
                frequency=choice(frequencies),
                start_date=choice(start_dates),
                price=round(uniform(1.99, 49.99), 2),
                currency=choice(currencies),
                comment='Generation date: ' + datetime.today().strftime("%d/%m/%Y, %H:%M:%S")
                )


class WrongCurrencyException(Exception):
    """Raises when the input currency is not supported"""
    pass
