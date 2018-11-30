import datetime
import hashlib
from typing import Iterator

def days_in_year(year: int) -> Iterator[datetime.date]:
    first_day_of_year = datetime.datetime(year=year, month=1, day=1).date()
    first_day_next_year = datetime.datetime(year=year+1, month=1, day=1).date()
    num_days_in_year = (first_day_next_year - first_day_of_year).days
    for curr_day in range(num_days_in_year):
        yield first_day_of_year + datetime.timedelta(days=curr_day)

def get_date_hash(date: datetime.date) -> int:
    """
    normal python hash function not stable between instances of python
    """
    return int(hashlib.sha256(str(date).encode("utf-8")).hexdigest(), 16)
