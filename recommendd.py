#!/usr/bin/env python3.7
import dio
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    sched = BlockingScheduler()
    first_run = datetime.datetime.now() + datetime.timedelta(seconds=10)
    sched.add_job(
            dio.main_recs,
            trigger='interval',
            days=1,
            misfire_grace_time=9000,
            coalesce=True,
            max_instances=1,
            next_run_time=first_run)
    sched.start()
