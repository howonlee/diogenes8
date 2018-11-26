from __future__ import annotations
import calendar
import os
import shutil
import json
import smtplib
import email
import random
import math
import datetime
import argparse
import dataclasses
import functools
from abc import ABC
from typing import Dict, Set, Any, IO, List, Optional

class DioDir(object):
    """
    Object corresponding to diogenes directory
    Note the default
    """
    def __init__(self, dirname=None):
        if not dirname:
            self.dirname = os.path.expanduser("~/.diogenes")
        else:
            self.dirname = str(dirname)

    def create_if_not_exists(self):
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

@dataclasses.dataclass
class Person(object):
    """
    We want a general data object, really
    """
    name: str
    email: str
    salt: str = str(random.randint(int(1e30), int(9e30)))

    def __hash__(self) -> int:
        return hash("{}_{}_{}".format(
                    self.name,
                    self.email,
                    self.salt))

    def to_file(self, person_filename: str) -> None:
        with open(person_filename, "w") as person_file:
            json.dump(dataclasses.asdict(self), person_file)

    def get_dir(self, dio_dir: DioDir) -> str:
        return dio_dir.dirname +\
                "/peep_{}".format(os.path.basename(self.name))

    def save(self, dio_dir: DioDir) -> None:
        """ upserts """
        peep_dirname = self.get_dir(dio_dir)
        if not os.path.exists(peep_dirname):
            os.makedirs(peep_dirname)
        peep_json_filename = Person.get_filename(peep_dirname)
        self.to_file(peep_json_filename)

    def delete(self, dio_dir: DioDir) -> None:
        peep_dirname = self.get_dir(dio_dir)
        if not os.path.exists(peep_dirname):
            raise Exception("Peep directory does not exist to delete")
        else:
            shutil.rmtree(peep_dirname)

    @staticmethod
    def get_filename(dirname: str) -> str:
        return os.path.join(dirname, "peep.json")

    @staticmethod
    def from_file(person_filename: str) -> Person:
        with open(person_filename, "r") as person_file:
            json_res: Dict[str, Any] = json.load(person_file)
            return Person(**json_res)

    @staticmethod
    def from_dir(person_dir: str) -> Person:
        person_filepath = Person.get_filename(person_dir)
        return Person.from_file(person_filepath)

    @staticmethod
    def is_peep_dir(dir_to_check: str) -> bool:
        parent_dir, filename = os.path.split(dir_to_check)
        if isinstance(filename, (bytes, bytearray)):
            filename = filename.decode(errors='replace')

        if filename.startswith("peep_"):
            return os.path.isdir(dir_to_check)
        else:
            return False
    
    @staticmethod
    def get_all(dio_dir: DioDir) -> List[Person]:
        dio_dir.create_if_not_exists()
        dirs = os.listdir(dio_dir.dirname)
        peep_dirs = filter(Person.is_peep_dir, dirs)
        return list(map(Person.from_dir, peep_dirs))


class ScheduleABC(ABC):
    def __init__(self):
        pass

    def should_email_day(self, dt: datetime.datetime) -> bool:
        """
        Returns True if we should email ourselves on day w/ reminders
        False otherwise
        """
        raise NotImplementedError()

    def next_emailing_day(self, dt: datetime.datetime) -> datetime.datetime:
        """
        Will shortcircuit if we are currently doing emailing day that day
        """
        curr_dt = dt
        while not self.should_email_day(curr_dt):
            curr_dt += datetime.timedelta(days=1)
        return curr_dt

    def should_contact(self, person: Person, dt: datetime.datetime) -> bool:
        raise NotImplementedError()


class ThreeTimesSchedule(ScheduleABC):
    """
    Email everyone over 8 weeks three times a year
    """
    def __init__(self):
        pass

    def should_email_day(self, dt: datetime.datetime) -> bool:
        _, weeknumber, weekday = dt.isocalendar()
        emailing_weeks = set(range(1, 9)) |\
                set(range(18,26)) |\
                set(range(35,43))
        if weeknumber in emailing_weeks:
            return True
        return False
    
    def next_emailing_day(self, dt: datetime.datetime) -> datetime.datetime:
        return super().next_emailing_day(dt)

    def should_contact(self, person: Person, dt: datetime.datetime) -> bool:
        _, weeknumber, weekday = dt.isocalendar()
        curr_emailing_week = weeknumber % 8
        curr_bucket = weekday + (weeknumber * 8)
        total_days_per_period = 8 * 7
        person_hash = hash(Person)
        return (person_hash % total_days_per_period) == curr_bucket

class DefaultSchedule(ScheduleABC):
    """
    Email everyone in a way that looks super random
    2x per year for everyone...
    """
    def __init__(self):
        pass

    def should_email_day(self, dt: datetime.datetime) -> bool:
        # use date, since otherwise the finer increments mess things up wrt stability
        # so, 20% of days, or about 75 days/year
        return hash(dt.date()) % 100 <= 20
    
    def next_emailing_day(self, dt: datetime.datetime) -> datetime.datetime:
        return super().next_emailing_day(dt)

    def set_of_days_emailed(self, year:int) -> Set[datetime.date]:
        first_day_of_year = datetime.datetime(year=year, month=1, day=1).date()
        res: Set[datetime.date] = set()
        for day in range(365):
            curr_day = first_day_of_year + datetime.timedelta(days=day)
            if self.should_email_day(
                    datetime.datetime.combine(
                        curr_day,
                        datetime.datetime.min.time()
                    )
                ):
                res.add(curr_day)
        return res

    @staticmethod
    def before_midyear(dt: datetime.date) -> bool:
        # midyear's day is july 2
        return dt < datetime.date(year=dt.year, month=7, day=2)

    @staticmethod
    def split_emailed_set(set_of_days: Set[datetime.date]) -> Tuple[Set[datetime.date], Set[datetime.date]]:
        return (sorted(list(filter(lambda x: DefaultSchedule.before_midyear(x), set_of_days))),
                sorted(list(filter(lambda x: not DefaultSchedule.before_midyear(x), set_of_days))))

    def should_contact(self, person: Person, dt: datetime.datetime) -> bool:
        days_emailed: Set[datetime.date] = self.set_of_days_emailed(dt.year)
        dt_date = dt.date()
        fst_emailed, snd_emailed = DefaultSchedule.split_emailed_set(days_emailed)
        person_hash = hash(Person)
        # assertion getting hit would not be happy
        assert dt_date in days_emailed
        email_list = fst_emailed if self.before_midyear(dt_date) else snd_emailed
        total_cardinality = len(email_list)
        curr_bucket = email_list.index(dt_date)
        return person_hash % total_cardinality == curr_bucket

def get_recs(dio_dir: DioDir, schedule: ScheduleABC, dt_to_rec: datetime.datetime) -> Optional[List[Person]]:
    if schedule.should_email_day(dt_to_rec):
        should_contact_on_day = functools.partial(
            schedule.should_contact,
            dt=dt_to_rec
        )
        return list(filter(should_contact_on_day, Person.get_all(dio_dir)))
    else:
        return None

def recs_to_message(res: Optional[List[Person]], next_day: datetime.date) -> str:
    if res is None:
        return "Next emailing day is : {}".format(next_day)
    elif res == []:
        return "Emailing day, but no peeps today. Add more peeps."
    else:
        return "\n".join(
            ["\t".join([peep.name, peep.email]) for peep in res]
        )

def send_message(contents: str) -> None:
    today: datetime.date = datetime.datetime.now().date()
    smtp_url: str = os.getenv("DIO_SMTP_URL", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("DIO_SMTP_PORT", "587"))
    smtp_username: str = os.environ["DIO_SMTP_USERNAME"]
    smtp_password: str = os.environ["DIO_SMTP_PASSWORD"]
    smtp_dest_email: str = os.environ["DIO_DEST_EMAIL"]
    msg_obj: email.message.EmailMessage = email.message.EmailMessage()
    msg_obj['From'] = smtp_username
    msg_obj['To'] = smtp_dest_email
    msg_obj['Subject'] = "Diogenes | {}".format(str(today))
    msg_obj.set_content(contents)
    with smtplib.SMTP(smtp_url, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg_obj)

def main_recs(send:bool=True) -> None:
    dio_dir: DioDir = DioDir()
    dio_dir.create_if_not_exists()
    sched: ScheduleABC = DefaultSchedule()
    today: datetime.datetime = datetime.datetime.now()
    res: Optional[List[Person]] = get_recs(dio_dir, sched, today)
    next_day: datetime.date = sched.next_emailing_day(today).date()
    message: str = recs_to_message(res, next_day)
    if send:
        send_message(message)
    else:
        print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand")
    parser.add_argument("--name")
    parser.add_argument("--email")
    parser.add_argument("--batchfile")
    args = parser.parse_args()
    if args.subcommand == "add":
        if not args.name:
            raise IOError("Needs a name")
        if not args.email:
            raise IOError("Needs an email")
        dio_dir = DioDir()
        dio_dir.create_if_not_exists()
        new_peep = Person(name=args.name, email=args.email)
        new_peep.save(dio_dir)
    elif args.subcommand == "batchadd":
        if not args.batchfile:
            raise IOError("Needs a batch file")
        if not args.batchfile.endswith("csv"):
            raise IOError("Needs a csv file")
        dio_dir = DioDir()
        dio_dir.create_if_not_exists()
        with open(args.batchfile, "r") as batch_file:
            reader = csv.DictReader(batch_files, fields=["name", "email"])
            for row in reader:
                new_peep = Person(name=row["name"], email=row["email"])
                new_peep.save(dio-dir)
    elif args.subcommand == "recs":
        print("You should probably use the recs daemon.")
        main_recs(send=False)
    else:
        raise NotImplementedError("Invalid command")
