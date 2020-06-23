from dataclasses import fields
from typing import Tuple
from random import choice, uniform
from dateutil.rrule import DAILY, WEEKLY, MONTHLY, YEARLY, rrule
from datetime import datetime
from pprint import pprint
# from subscription_manager.subscription import Subscription
from subscription_manager.subscription import Subscription


def _get_currencies_list() -> Tuple[str]:
    """
    Return list of supported currencies.
    Returns:
        tuple: list of supported currencies
    """
    return 'USD', 'GBP', 'EUR', 'RUB', 'CNY'


def _get_frequencies_list() -> Tuple[str]:
    """
    Return list of supported frequencies.
    Returns:
        tuple: list of supported currencies
    """
    return 'daily', 'weekly', 'monthly', 'yearly'


def subscription_generator() -> dict:
    """
    Generate subscription with correct fields.
    Returns:
        subscription (dict): generated subscription
    """
    names = ['Mary', 'Eva', 'Nancy', 'Ann', 'Kevin', 'John', 'Ben', 'Robin']
    currencies = _get_currencies_list()
    frequencies = _get_frequencies_list()
    subscription_names = ['Google music', 'Spotify', 'Apple Music', 'Youtube Music', 'Coursera', 'Pluralsight',
                          'Amazon Prime', 'Netflix', 'Sky Store', 'Pet insurance', 'Mobile payment']
    start_dates = list(
        rrule(WEEKLY, dtstart=datetime(2018, 9, 1).date(), until=datetime.today().date()))
    return dict(owner=choice(names),
                name=choice(subscription_names),
                frequency=choice(frequencies),
                start_date=choice(start_dates),
                price=round(uniform(1.99, 49.99), 2),
                currency=choice(currencies),
                comment="Generation date: " + datetime.today().strftime("%d/%m/%Y, %H:%M:%S")
                )


def validate_subscription(subscription: dict) -> Subscription:
    """
    Take subscription and validate its every field
    Args:
        subscription (dict): subscription to validate
    Returns:
        True: in case of valid subscription
        False: in case of invalid subscription
    Raises:
        MissingFieldsException: If some of mandatory fields is missing
        WrongCurrencyException: If input currency is not supported
    """
    # Check that there is no missed fields in the subscription
    expected_fields = {field.name: field.type for field in fields(Subscription)}
    if subscription.keys() != expected_fields.keys():
        raise MissingFieldsException("Some fields in the taken subscription are missing")

    # Check that types of all fields are correct
    for key, value in subscription.items():
        if type(value) != expected_fields[key]:
            raise InvalidSubsFieldException(
                f"Found wrong field type, expected:{expected_fields[key]}, received:{type(value)}")

    # Check that given subscription currency is supported
    supported_currencies = _get_currencies_list()
    if subscription['currency'] not in supported_currencies:
        raise InvalidSubsFieldException("Unexpected currency was found, supported currencies: ",
                                        " ".join(supported_currencies))

    # Check that given subscription frequency is supported
    supported_frequencies = _get_frequencies_list()
    if subscription['frequency'] not in supported_frequencies:
        raise InvalidSubsFieldException("Unexpected frequency was found, supported frequencies: ",
                                        " ".join(supported_frequencies))

    # Check that start_date is less than today
    if subscription['start_date'] > datetime.today():
        raise InvalidSubsFieldException("Start dates in the future are not supported")
    return True


sub_dict = subscription_generator()
validate_subscription(sub_dict)


class MissingFieldsException(Exception):
    """Raises when some fields in subscription are missed"""


class WrongFrequencyException(Exception):
    """Raised when the input value is too small"""


class SubsNotFoundException(Exception):
    """Raises when the input subscription was not found"""


class InvalidSubsFieldException(Exception):
    """Raises when taken subscription is invalid"""
