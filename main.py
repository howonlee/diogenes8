from __future__ import annotations
import functools
import csv
import random
import email
import smtplib
import argparse
import datetime
from dio import *
from typing import Optional, Any, Dict, List

def main_recs(send:bool=True) -> None:
    dio_dir: DioDir = DioDir()
    dio_dir.create_if_not_exists()
    sched: ScheduleABC = DefaultSchedule()
    today: datetime.date = datetime.datetime.now().date()
    res: Optional[List[Person]] = get_recs(dio_dir, sched, today)
    next_day: datetime.date = sched.next_emailing_day(today)
    message: str = recs_to_message(res, next_day)
    if send:
        settings: Optional[Settings] = dio_dir.get_settings()
        assert settings is not None, "Have to set settings"
        send_message(message, today, settings)
    else:
        print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand")
    parser.add_argument("--name")
    parser.add_argument("--batchfile")
    args = parser.parse_args()
    if args.subcommand == "add":
        if not args.name:
            raise IOError("Needs a name")
        dio_dir = DioDir()
        dio_dir.create_if_not_exists()
        new_peep = Person(name=args.name)
        new_peep.save(dio_dir)
    elif args.subcommand == "batchadd":
        if not args.batchfile:
            raise IOError("Needs a batch file")
        if not args.batchfile.endswith("csv"):
            raise IOError("Needs a csv file")
        dio_dir = DioDir()
        dio_dir.create_if_not_exists()
        with open(args.batchfile, "r") as batch_file:
            reader = csv.DictReader(batch_file, fieldnames=["name"])
            for row in reader:
                # if you don't do this they all have the same salt
                new_rand = str(random.randint(int(1e30), int(9e30)))
                new_peep = Person(name=row["name"], salt=new_rand)
                new_peep.save(dio_dir)
    elif args.subcommand == "dryrecs":
        print("Recommendations for today, no email.")
        main_recs(send=False)
    elif args.subcommand == "recs":
        print("Recommendations for today sent by email.")
        main_recs(send=True)
    elif args.subcommand == "setup":
        dio_dir = DioDir()
        dio_dir.create_if_not_exists()
        dio_dir.set_settings_interactive()
    else:
        raise NotImplementedError("Invalid command")
