import datetime
from typing import Iterator

def days_in_year(year: int) -> Iterator[datetime.date]:
    first_day_of_year = datetime.datetime(year=year, month=1, day=1).date()
    first_day_next_year = datetime.datetime(year=year+1, month=1, day=1).date()
    num_days_in_year = (first_day_next_year - first_day_of_year).days
    for curr_day in range(num_days_in_year):
        yield first_day_of_year + datetime.timedelta(days=curr_day)
