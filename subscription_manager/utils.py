from dataclasses import fields
from typing import Tuple
from random import choice, uniform, randint
from datetime import datetime, date
from subscription_manager.exceptions import *
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
    # generate random day from the beginning of the current year to today
    start_dt = date.today().replace(day=1, month=1).toordinal()
    end_dt = date.today().toordinal()
    random_day = date.fromordinal(randint(start_dt, end_dt))

    return dict(owner=choice(names),
                name=choice(subscription_names),
                frequency=choice(frequencies),
                start_date=random_day,
                price=round(uniform(1.99, 49.99), 2),
                currency=choice(currencies),
                comment="Generation date: " + datetime.today().strftime("%d/%m/%Y, %H:%M:%S")
                )


def validate_subscription(subscription: dict) -> bool:
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
                f"Found wrong field type, expected:{expected_fields[key]}, received:{type(value), value}")

    # Check that given subscription currency is supported
    supported_currencies = _get_currencies_list()
    if subscription['currency'] not in supported_currencies:
        raise InvalidSubsFieldException(f"Unexpected currency: {subscription['frequency']}, supported currencies: ",
                                        " ".join(supported_currencies))

    # Check that given subscription frequency is supported
    supported_frequencies = _get_frequencies_list()
    if subscription['frequency'] not in supported_frequencies:
        raise InvalidSubsFieldException(f"Unexpected frequency: {subscription['frequency']}, supported frequencies: ",
                                        " ".join(supported_frequencies))

    # Check that start_date is less than today
    if subscription['start_date'] > date.today():
        raise InvalidSubsFieldException("Start dates in the future are not supported")
    return True
