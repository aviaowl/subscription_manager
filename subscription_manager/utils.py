from typing import List


def _validate_subscription(subscription: dict) -> bool:
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


class WrongCurrencyException(Exception):
    """Raises when the input currency is not supported"""
    pass
