import subscription_manager.utils as utils
from subscription_manager.dbhelper import DBHelper
from subscription_manager.utils import SubscriptionException
from typing import List


class Controller:
    """Class for creation, validation, edition, deletion and getting of subscription objects"""

    def __init__(self, dbhelper: DBHelper):
        """Takes DBHelper instance for communicating with database"""
        self.dbhelper = dbhelper

    def add_subscription(self, subscription_dict: dict) -> int:
        """
        Add subscription to database.
        Validates subscription, creates instance of Subscription class and send it to DBHelper
        Args:
            subscription_dict (dict): subscription to add
        Examples:
            {"owner": 'Lena',
             "name": 'Amazon Prime',
             "frequency": '1 month',
             "start_date": datetime.datetime(2020, 6, 18),
             "price": 8.99,
             "currency": 'GBP',
             "comment": 'Prime membership for faster delivery'}
        Returns:
            int: identifier of created subscription
        """
        try:
            subscription_obj = utils.create_subscription(**subscription_dict)
        except SubscriptionException as exc:
            raise exc
        result_id = self.dbhelper.add_subscription(subscription_obj)
        return result_id

    def edit_subscription(
            self, subscription_id: int, subscription_changes: dict
    ) -> int:
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
            SubsNotFoundException: when subscription with this id doesn't exist in database
        """
        pass

    def get_subscription_by_id(self, subscription_id: int) -> dict:
        """
        Return subscription by identifier
        Returns:
            dict: found subscription in dict representation
        Raises:
            SubsNotFoundException: when subscription with this id doesn't exist in database
        """
        pass

    def _get_subscription_id(self, subscription_name: str) -> int:
        """
        Search subscription by its name and return its identifier
        Args:
            subscription_name (str): name of subscription to search
        Returns:
            int: identifier of found subscription
        Raises:
            SubsNotFoundException: when subscription was not found in database
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
