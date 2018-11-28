import dio
import utils
import datetime
from typing import List, Optional

"""
Lists what all the recommendations are going to be this year
"""

def list_all_recs(dio_dir: dio.DioDir, sched: dio.ScheduleABC, year: int) -> List[Optional[List[dio.Person]]]:
    datetimes_in_year = map(
            lambda x: datetime.datetime.combine(x, datetime.datetime.min.time()),
            utils.days_in_year(year)
            )
    return list(
            map(
                lambda x: dio.get_recs(dio_dir, sched, x),
                datetimes_in_year
                )
            )

if __name__ == "__main__":
    dio_dir = dio.DioDir()
    sched = dio.DefaultSchedule()
    curr_year = datetime.datetime.now().year
    print(list_all_recs(dio_dir, sched, curr_year))

