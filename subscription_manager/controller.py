import subscription_manager.utils as utils
from subscription_manager.dbhelper import DBHelper
from subscription_manager.subscription import Subscription
from subscription_manager.utils import SubscriptionException
from subscription_manager.exceptions import (
    WrongTypeException,
    InvalidValueException,
)
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

    def get_subscription_by_name(self, subscription_name: str) -> Subscription:
        """
        Return subscription by name
        Returns:
            <class Subscription>: found subscription like Subscription object
        Raises:
            SubsNotFoundException: when subscription with this id doesn't exist in database
        """
        if type(subscription_name) is not str:
            raise WrongTypeException(
                f"Found wrong field 'subscription_name' type, expected: <str>, received: {type(subscription_name), subscription_name}"
            )
        if len(subscription_name) < 1:
            raise InvalidValueException(
                "Subscription name length should be more than one"
            )
        received_subscription: dict = self.dbhelper.get_subscription(subscription_name)
        received_subscription.update({"start_date": received_subscription["start_date"].date()})
        return Subscription(**received_subscription)

    def get_subscriptions_list(self, owner=None) -> List[Subscription]:
        """
        Return list of subscriptions
        Args:
            owner (str): not mandatory, if not None returns all subscriptions of specified owner
        Returns:
            List[Subscription]: list of all subscriptions or all user's subscription if owner is specified
        """
        if type(owner) is not str and owner is not None:
            raise WrongTypeException(
                f"Found wrong owner name's type, expected: <str>, received: {type(owner), owner}"
            )
        if owner == "":
            owner = None
        subscription_list = self.dbhelper.get_all_subscriptions(owner)
        # Convert start_date type from datetime to date, convert every dict to Subscription
        for i, sub_dict in enumerate(subscription_list):
            sub_dict.update({"start_date": sub_dict["start_date"].date()})
            subscription_list[i] = Subscription(**sub_dict)
        return subscription_list
