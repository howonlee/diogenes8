import datetime

class DefaultSchedule(ScheduleABC):
    """
    Email everyone in a way that looks super random
    2x per year for everyone...
    """
    def __init__(self):
        pass

    def should_email_day(self, date: datetime.date) -> bool:
        # use date, since otherwise the finer increments mess things up wrt stability
        # so, 25% of days, or about 90 days/year
        return utils.get_date_hash(date) % 100 <= 25
    
    def next_emailing_day(self, date: datetime.date) -> datetime.date:
        return super().next_emailing_day(date)

    def set_of_days_emailed(self, year:int) -> Iterator[datetime.date]:
        return filter(self.should_email_day, utils.days_in_year(year))

    @staticmethod
    def before_midyear(date: datetime.date) -> bool:
        # midyear's day is july 2
        return date < datetime.date(year=date.year, month=7, day=2)

    @staticmethod
    def split_emailed_set(set_of_days: Set[datetime.date]) -> Tuple[List[datetime.date], List[datetime.date]]:
        return (sorted(list(filter(lambda x: DefaultSchedule.before_midyear(x), set_of_days))),
                sorted(list(filter(lambda x: not DefaultSchedule.before_midyear(x), set_of_days))))

    def should_contact(self, person: Person, date: datetime.date) -> bool:
        days_emailed: Set[datetime.date] = set(self.set_of_days_emailed(date.year))
        fst_emailed, snd_emailed = DefaultSchedule.split_emailed_set(days_emailed)
        # assertion getting hit would not be happy
        assert date in days_emailed
        email_list = fst_emailed if self.before_midyear(date) else snd_emailed
        total_cardinality = len(email_list)
        curr_bucket = email_list.index(date)
        return hash(person) % total_cardinality == curr_bucket

