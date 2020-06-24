from dataclasses import dataclass
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, WEEKLY, MONTHLY, YEARLY, rrule


@dataclass
class Subscription:
    """Data class for Subscription representation
        Attributes:
            owner (str): name of the person, who owns this subscription.
            name (str): name of the subscription, e.g. 'Spotify music'
            frequency (str): payment period for subscription from the list: daily, weekly, monthly, yearly
            start_date (date): date when subscription started
            price (str): amount of money needed to pay for subscription per one payment period
            currency (str): currency of payment, default GBP
            comment (str): not-mandatory comment for subscription
        Methods:
            get_next_payment_date (datetime): returns next payment date for the subscription
    """
    owner: str
    name: str
    frequency: str
    start_date: date
    price: float
    currency: str
    comment: str

    def __str__(self):
        return f'({self.owner}, ' \
               f'{self.name}, ' \
               f'{self.frequency}, ' \
               f'{self.start_date}, ' \
               f'{self.price}, ' \
               f'{self.currency}, ' \
               f'{self.comment})'

    def get_next_payment_date(self) -> datetime:
        """Return next payment day, that is bigger or equal than today
            Returns:
                datetime: date of the next payment. Example: 'datetime(2020, 06, 18)'
        """
        today = date.today()
        # dict contains sequence of dates since start_date until today+selected period.
        # for example, if today = Jun 03,2020 and start_date = Jun 01, 2020 and frequency = 'DAILY',
        # periods[daily] contains Jun 01, 2020; Jun 02,2020; Jun 03, 2020, Jun 04, 2020 in datetime format
        periods = dict(daily=list(rrule(DAILY, dtstart=self.start_date, until=today + relativedelta(days=1))),
                       weekly=list(rrule(WEEKLY, dtstart=self.start_date, until=today + relativedelta(weeks=1))),
                       monthly=list(rrule(MONTHLY, dtstart=self.start_date, until=today + relativedelta(months=1))),
                       yearly=list(rrule(YEARLY, dtstart=self.start_date, until=today + relativedelta(years=1))))
        # if payment date is today, return today, else - next payment day in the future
        if periods[self.frequency][-2].date() == today:
            return today
        else:
            return periods[self.frequency][-1].date()
