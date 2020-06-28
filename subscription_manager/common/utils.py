from dataclasses import fields
from datetime import datetime, date
from random import choice, uniform, randint

from subscription_manager.common.constants import *
from subscription_manager.common.exceptions import *
from subscription_manager.subscription import Subscription


def subscription_generator() -> dict:
    """
    Generate subscription with correct fields.
    Returns:
        subscription (dict): generated subscription
    """
    names = ["Mary", "Eva", "Nancy", "Ann", "Kevin", "John", "Ben", "Robin"]
    subscription_names = [
        "Google music",
        "Spotify",
        "Apple Music",
        "Youtube Music",
        "Coursera",
        "Pluralsight",
        "Amazon Prime",
        "Netflix",
        "Sky Store",
        "Pet insurance",
        "Mobile payment",
    ]
    # generate random day from the beginning of the current year to today
    start_dt = date.today().replace(day=1, month=1).toordinal()
    end_dt = date.today().toordinal()
    random_day = date.fromordinal(randint(start_dt, end_dt))

    return dict(
        owner=choice(names),
        name=choice(subscription_names),
        frequency=choice(FREQUENCIES),
        start_date=random_day,
        price=round(uniform(1.99, 49.99), 2),
        currency=choice(CURRENCIES),
        comment="Generation date: " + datetime.today().strftime("%d/%m/%Y, %H:%M:%S"),
    )


def create_subscription(**params) -> Subscription:
    """
    Take subscription, validate its every field and return Subscription object
    Args:
        **params: subscription to create
    The format for a parameter is:
            owner (str): name of the person, who owns this subscription.
            name (str): name of the subscription, e.g. 'Spotify music'
            frequency (str): payment period for subscription from the list: daily, weekly, monthly, yearly
            start_date (date): date when subscription started
            price (str): amount of money needed to pay for subscription per one payment period
            currency (str): currency of payment
            comment (str): not-mandatory comment for subscription
    Returns:
        class <Subscription>: subscription object in case of valid input
    Raises:
        MissingFieldsException: If some of mandatory fields is missing
        InvalidValueException: If some of taken fields have invalid values
        WrongTypeException: If some of taken fields have wrong types
    """
    # Check that there is no missed fields in the subscription
    expected_fields = {field.name: field.type for field in fields(Subscription)}
    if params.keys() != expected_fields.keys():
        raise MissingFieldsException(MISSING_FIELDS_MSG)

    # Check that types of all fields are correct
    for key, value in params.items():
        if type(value) != expected_fields[key]:
            raise WrongTypeException(
                WRONG_TYPE_MSG.format(
                    expected=expected_fields[key],
                    recieved_type=type(value),
                    field=value,
                )
            )

    # Check that given subscription currency is supported
    if params["currency"] not in CURRENCIES:
        raise InvalidValueException(
            UNEXPECTED_CURRENCY_MSG.format(currency=params["currency"])
        )

    # Check that given subscription frequency is supported
    if params["frequency"] not in FREQUENCIES:
        raise InvalidValueException(
            UNEXPECTED_FREQUENCY_MSG.format(frequency=params["frequency"])
        )

    # Check that start_date is less than today
    if params["start_date"] > date.today():
        raise InvalidValueException(FUTURE_START_DATE_MSG)
    return Subscription(**params)


def validate_str_field(field: str, none_allowed: bool = False):
    """
    Args:
        field (str): field to validate
        none_allowed (bool): If True then None value of the field is allowed, else raise exception
    Returns:
        None
    Raises:
        WrongTypeException: If field type is not string and not None (depends on none_allowed)
        InvalidValueException: If field is empty
    """
    if not isinstance(field, str) and field is not None:
        raise WrongTypeException(
            WRONG_TYPE_MSG.format(expected=str, recieved_type=type(field), field=field)
        )
    if not none_allowed and field is None:
        print(none_allowed, field)
        raise WrongTypeException(
            WRONG_TYPE_MSG.format(expected=str, recieved_type=type(field), field=field)
        )
    if field == "":
        raise InvalidValueException(EMPTY_FIELD_MSG)
