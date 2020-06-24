from dataclasses import fields
from random import choice, uniform, randint
from datetime import datetime, date
from subscription_manager.exceptions import *
from subscription_manager.subscription import Subscription
import subscription_manager.const as const


def subscription_generator() -> dict:
    """
    Generate subscription with correct fields.
    Returns:
        subscription (dict): generated subscription
    """
    names = ['Mary', 'Eva', 'Nancy', 'Ann', 'Kevin', 'John', 'Ben', 'Robin']
    subscription_names = ['Google music', 'Spotify', 'Apple Music', 'Youtube Music', 'Coursera', 'Pluralsight',
                          'Amazon Prime', 'Netflix', 'Sky Store', 'Pet insurance', 'Mobile payment']
    # generate random day from the beginning of the current year to today
    start_dt = date.today().replace(day=1, month=1).toordinal()
    end_dt = date.today().toordinal()
    random_day = date.fromordinal(randint(start_dt, end_dt))

    return dict(owner=choice(names),
                name=choice(subscription_names),
                frequency=choice(const.FREQUENCIES),
                start_date=random_day,
                price=round(uniform(1.99, 49.99), 2),
                currency=choice(const.CURRENCIES),
                comment="Generation date: " + datetime.today().strftime("%d/%m/%Y, %H:%M:%S")
                )


def create_subscription(**subscription) -> Subscription:
    """
    Take subscription, validate its every field and return Subscription object
    Args:
        subscription (dict): subscription to create
    Returns:
        class <Subscription>: subscription object in case of valid input
    Raises:
        MissingFieldsException: If some of mandatory fields is missing
        InvalidValueException: If some of taken fields have invalid values
        WrongTypeException: If some of taken fields have wrong types
    """
    # Check that there is no missed fields in the subscription
    expected_fields = {field.name: field.type for field in fields(Subscription)}
    if subscription.keys() != expected_fields.keys():
        raise MissingFieldsException("Some fields in the taken subscription are missing")

    # Check that types of all fields are correct
    for key, value in subscription.items():
        if type(value) != expected_fields[key]:
            raise WrongTypeException(
                f"Found wrong field '{key}' type, expected:{expected_fields[key]}, received:{type(value), value}")

    # Check that given subscription currency is supported
    if subscription['currency'] not in const.CURRENCIES:
        raise InvalidValueException(f"Unexpected currency: {subscription['frequency']}, supported currencies: ",
                                    " ".join(const.CURRENCIES))

    # Check that given subscription frequency is supported
    if subscription['frequency'] not in const.FREQUENCIES:
        raise InvalidValueException(f"Unexpected frequency: {subscription['frequency']}, supported frequencies: ",
                                    " ".join(const.FREQUENCIES))

    # Check that start_date is less than today
    if subscription['start_date'] > date.today():
        raise InvalidValueException("Start dates in the future are not supported")
    return Subscription(**subscription)
