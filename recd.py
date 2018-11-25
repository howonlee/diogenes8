import dio
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.add_job(dio.send_recs, 'interval', days=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
