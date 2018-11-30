import datetime
from .schedule_abc import ScheduleABC
from .person import Person


class ThreeTimesSchedule(ScheduleABC):
    """
    Email everyone over 8 weeks three times a year
    """
    def __init__(self):
        pass

    def should_email_day(self, date: datetime.date) -> bool:
        dt = datetime.datetime.combine(date, datetime.datetime.min.time())
        _, weeknumber, weekday = dt.isocalendar()
        emailing_weeks = set(range(1, 9)) |\
                set(range(18,26)) |\
                set(range(35,43))
        if weeknumber in emailing_weeks:
            return True
        return False
    
    def next_emailing_day(self, date: datetime.date) -> datetime.date:
        return super().next_emailing_day(date)

    def should_contact(self, person: Person, date: datetime.date) -> bool:
        dt = datetime.datetime.combine(date, datetime.datetime.min.time())
        _, weeknumber, weekday = dt.isocalendar()
        curr_emailing_week = weeknumber % 8
        curr_bucket = weekday + (weeknumber * 8)
        total_days_per_period = 8 * 7
        return (hash(person) % total_days_per_period) == curr_bucket

