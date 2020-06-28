from typing import List

import subscription_manager.common.utils as utils
from subscription_manager.common.exceptions import SubscriptionException
from subscription_manager.dbhelper import DBHelper
from subscription_manager.subscription import Subscription


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
        except SubscriptionException:
            raise
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

    def delete_subscription(self, subscription_name: str) -> int:
        """
        Delete subscription by name
        Args:
            subscription_name (str): identifier of subscription to delete
        Returns:
            int: count of deleted subscriptions
        """
        try:
            utils.validate_str_field(field=subscription_name)
        except SubscriptionException:
            raise
        deleted_subscriptions_count = self.dbhelper.delete_subscription(
            subscription_name
        )
        return deleted_subscriptions_count

    def get_subscription_by_name(self, subscription_name: str) -> Subscription:
        """
        Return subscription by name
        Returns:
            <class Subscription>: found subscription like Subscription object
        Raises:
            SubsNotFoundException: when subscription with this id doesn't exist in database
        """
        try:
            utils.validate_str_field(field=subscription_name)
        except SubscriptionException:
            raise
        received_subscription: dict = self.dbhelper.get_subscription(subscription_name)
        return Subscription(**received_subscription)

    def get_subscriptions_list(self, owner: str = None) -> List[Subscription]:
        """
        Return list of subscriptions
        Args:
            owner (str): not mandatory, if not None returns all subscriptions of specified owner
        Returns:
            List[Subscription]: list of all subscriptions or all user's subscription if owner is specified
        """
        try:
            utils.validate_str_field(field=owner, none_allowed=True)
        except SubscriptionException:
            raise
        subscription_list = self.dbhelper.get_all_subscriptions(owner)
        # Convert start_date type from datetime to date, convert every dict to Subscription
        return [Subscription(**subscription) for subscription in subscription_list]
