from dataclasses import dataclass
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, WEEKLY, MONTHLY, YEARLY, rrule


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

    def get_next_payment_date(self, start_date: datetime, frequency: str) -> datetime:
        """Return next payment day, that is bigger or equal than today
            Arguments:
                start_date (datetime): day, when subscription started. Example: datetime.datetime(2020, 3, 26)
                frequency (str): payment frequency. Possible values: daily, weekly, monthly, yearly
            Returns:
                pay_day (datetime): date of the next payment. Example: 'datetime(2020, 06, 18)'
        """
        if frequency.lower() not in ('daily', 'weekly', 'monthly', 'yearly'):
            raise WrongFrequency(
                'Unable to parse frequency: expected format examples: daily, weekly, monthly, yearly')
        today = datetime.today().date()
        # dict contains sequence of dates since start_date until today+selected period.
        # for example, if today = Jun 03,2020 and start_date = Jun 01, 2020 and frequency = 'DAILY',
        # periods[daily] contains Jun 01, 2020; Jun 02,2020; Jun 03, 2020, Jun 04, 2020 in datetime format
        periods = dict(daily=list(rrule(DAILY, dtstart=start_date, until=today + relativedelta(days=1))),
                       weekly=list(rrule(WEEKLY, dtstart=start_date, until=today + relativedelta(weeks=1))),
                       monthly=list(rrule(MONTHLY, dtstart=start_date, until=today + relativedelta(months=1))),
                       yearly=list(rrule(YEARLY, dtstart=start_date, until=today + relativedelta(years=1))))
        print('\n', periods[frequency][-2].date())
        if periods[frequency][-2].date() == today:
            return today
        else:
            return periods[frequency][-1].date()


class WrongFrequency(Exception):
    """Raised when the input value is too small"""
    pass
