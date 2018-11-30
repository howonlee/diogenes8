from abc import ABC
import datetime
from person import Person

class ScheduleABC(ABC):
    def __init__(self):
        pass

    def should_email_day(self, date: datetime.date) -> bool:
        """
        Returns True if we should email ourselves on day w/ reminders
        False otherwise
        """
        raise NotImplementedError()

    def next_emailing_day(self, date: datetime.date) -> datetime.date:
        """
        Will shortcircuit if we are currently doing emailing day that day
        """
        curr_dt = date
        while not self.should_email_day(curr_dt):
            curr_dt += datetime.timedelta(days=1)
        return curr_dt

    def should_contact(self, person: Person, date: datetime.date) -> bool:
        raise NotImplementedError()


