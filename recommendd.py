import dio
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.add_job(dio.main_recs, 'interval', days=1)
    scheduler.start()
