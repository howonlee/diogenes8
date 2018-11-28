import dio
import utils
import datetime
from typing import List, Optional

"""
Lists what all the recommendations are going to be this year

Rather spoils the surprise a bit, but still here for testing reasons
"""

def list_all_recs(dio_dir: dio.DioDir, sched: dio.ScheduleABC, year: int) -> List[Optional[List[dio.Person]]]:
    return list(
            map(
                lambda x: dio.get_recs(dio_dir, sched, x),
                utils.days_in_year(year)
                )
            )

if __name__ == "__main__":
    dio_dir = dio.DioDir()
    sched = dio.DefaultSchedule()
    curr_year = datetime.datetime.now().year
    all_recs = list_all_recs(dio_dir, sched, curr_year)
    for day, recs in zip(utils.days_in_year(curr_year), all_recs):
        print("day: {} - recs: {}".format(str(day), str(recs)))

