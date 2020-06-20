import datetime
from dataclasses import dataclass


@dataclass
class Subscription:
    """Data class for Subscription representation
        Attributes:
            owner (str) - name of the person, who owns this subscription.
            name (str) - name of the subscription, e.g. 'Spotify music'
            frequency (str) - payment period for subscription, e.g. 1 month
            price (str) - amount of money needed to pay for subscription per one payment period
            currency (str) - currency of payment, default GBP
            comment(str) - not-mandatory comment for subscription
        Methods:
            No methods
    """
    owner: str
    name: str
    frequency: str
    start_date: datetime
    price: float
    currency: str
    comment: str

    def __str__(self):
        return f"({self.owner}, " \
               f"{self.name}, " \
               f"{self.frequency}, " \
               f"{self.start_date}, " \
               f"{self.price}, " \
               f"{self.currency}, " \
               f"{self.comment})"
