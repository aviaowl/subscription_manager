from subscription_manager.DBHelper import DBHelper
from typing import List


class Controller:
    """Class for creation, validation, edition, deletion and getting of subscription objects"""

    def __init__(self, dbhelper: DBHelper):
        """Takes DBHelper instance for communicating with database"""
        self.dbhelper = dbhelper

    def add_subscription(self, subscription: dict) -> int:
        """
        Add subscription to database.
        Validates subscription, creates instance of Subscription class and send it to DBHelper
        Args:
            subscription (dict):
        Examples:
            {"owner": 'Lena',
             "name": 'Amazon Prime',
             "frequency": '1 month',
             "start_date": datetime.datetime(2020, 6, 18),
             "price": 8.99,
             "currency": 'GBP',
             "comment": 'Prime membership for faster delivery'}
        Returns:
            id (int): id of created subscription
        """
        pass

    def edit_subscription(self, subscription_id: int, subscription_changes: dict) -> int:
        """
        Validate changes and edit subscription in database
        Args:
            subscription_id (int):
            subscription_changes (dict):
        Examples:
            id=1,
            {"price": 8.99,
             "comment": 'Price has been increased since Jun, 21'}
        Returns:
            id (int): identifier of changed subscription
        """
        pass

    def delete_subscription(self, subscription_id: int) -> int:
        """
        Delete subscription by identifier
        Args:
            subscription_id (int): identifier of subscription to delete
        Returns:
            int: identifier of deleted subscription
        Raises:
            SubsNotFoundError: when subscription with this id doesn't exist in database
        """
        pass

    def get_subscription_by_id(self, subscription_id: int) -> dict:
        """
        Return subscription by identifier
        Returns:
            dict: found subscription in dict representation
        Raises:
            SubsNotFoundError: when subscription with this id doesn't exist in database
        """
        pass

    def _get_subscription_id(self, subscription: dict) -> int:
        """
        Search subscription by its fields and return its identifier
        Returns:
            int: identifier of found subscription
        Raises:
            SubsNotFoundError: when subscription was not found in database
        """
        pass

    def get_subscriptions_list(self, owner=None) -> List[dict]:
        """
        Return list of subscriptions
        Args:
            owner (str): not mandatory, if not None returns all subscriptions of specified owner
        Returns:
            List[dict]:
        """
        pass

    def _validate_subscription(self, subscription: dict) -> bool:
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

    @staticmethod
    def _get_currencies_list() -> List[str]:
        """
        Return list of supported currencies.
        Returns:
            currencies (list): list of supported currencies
        """
        return 'USD', 'GBP', 'EUR', 'RUB', 'CNY'


class WrongCurrencyError(Exception):
    """Raises when the input currency is not supported"""
    pass


class SubsNotFoundError(Exception):
    """Raises when the input subscription was not found"""
    pass
