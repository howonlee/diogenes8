from __future__ import annotations
import calendar
import os
import shutil
import getpass
import csv
import json
import smtplib
import hashlib
import email
import random
import math
import datetime
import argparse
import dataclasses
import functools
import utils
from abc import ABC
from typing import Dict, Set, Any, Tuple, IO, List, Optional, Iterator

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

    def get_settings_filename(self) -> str:
        filename = "{}_settings.json".format(getpass.getuser())
        return os.path.join(self.dirname, filename)

    def get_settings(self) -> Optional[Settings]:
        settings_filename = self.get_settings_filename()
        if os.path.isfile(settings_filename):
            return Settings.from_file(settings_filename)
        else:
            return None

    def get_settings_interactive(self) -> Settings:
        """
        try to get settings.
        if fail, then interactively set them and get them
        """
        res = self.get_settings()
        if res is None:
            return self.set_settings_interactive()
        else:
            return res

    def set_settings(self, new_settings: Settings) -> Settings:
        settings_filename = self.get_settings_filename()
        new_settings.to_file(settings_filename)
        return new_settings

    def set_settings_interactive(self) -> Settings:
        settings_filename = self.get_settings_filename()
        smtp_username = input("SMTP username (your webmail username, usually")
        smtp_password = input("SMTP app password (for gmail, see https://support.google.com/accounts/answer/185833")
        smtp_dest_email = input("Destination email. Can be same or different from SMTP username.")
        smtp_url = input("SMTP url [smtp.gmail.com]")
        smtp_port = input("SMTP port [587]")
        new_settings = Settings(smtp_username=smtp_username,
                                smtp_password=smtp_password,
                                smtp_dest_email=smtp_dest_email,
                                smtp_url=smtp_url,
                                smtp_port=int(smtp_port))
        new_settings.to_file(settings_filename)
        return new_settings

    def create_if_not_exists(self):
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

@dataclasses.dataclass
class Settings(object):
    smtp_username: str
    smtp_password: str
    smtp_dest_email: str
    smtp_url: str = "smtp.gmail.com"
    smtp_port: int = 587

    def to_file(self, settings_filename: str) -> None:
        with open(settings_filename, "w") as settings_file:
            json.dump(dataclasses.asdict(self), settings_file)

    @staticmethod
    def from_file(settings_filename: str) -> Settings:
        with open(settings_filename, "r") as settings_file:
            json_res: Dict[str, Any] = json.load(settings_file)
            return Settings(**json_res)


@dataclasses.dataclass
class Person(object):
    name: str
    salt: str = str(random.randint(int(1e30), int(9e30)))

    def __hash__(self) -> int:
        """
        Don't use a more normal hash dealie, it's not stable between Python instances
        """
        return int(self.salt)

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
    def get_all(dio_dir: DioDir) -> List[Person]:
        dio_dir.create_if_not_exists()
        res = []
        for dirpath, _, filenames in os.walk(dio_dir.dirname):
            if "peep_" in dirpath and "peep.json" in filenames:
                res.append(Person.from_dir(dirpath))
        return res


class ScheduleABC(ABC):
    def __init__(self):
        pass

    def should_email_day(self, date: datetime.date) -> bool:
        """
        Returns True if we should email ourselves on day w/ reminders
        False otherwise
        """
        raise NotImplementedError()

    def next_emailing_day(self, date: datetime.date) -> datetime.date:
        """
        Will shortcircuit if we are currently doing emailing day that day
        """
        curr_dt = date
        while not self.should_email_day(curr_dt):
            curr_dt += datetime.timedelta(days=1)
        return curr_dt

    def should_contact(self, person: Person, date: datetime.date) -> bool:
        raise NotImplementedError()


class ThreeTimesSchedule(ScheduleABC):
    """
    Email everyone over 8 weeks three times a year
    """
    def __init__(self):
        pass

    def should_email_day(self, date: datetime.date) -> bool:
        dt = datetime.datetime.combine(date, datetime.datetime.min.time())
        _, weeknumber, weekday = dt.isocalendar()
        emailing_weeks = set(range(1, 9)) |\
                set(range(18,26)) |\
                set(range(35,43))
        if weeknumber in emailing_weeks:
            return True
        return False
    
    def next_emailing_day(self, date: datetime.date) -> datetime.date:
        return super().next_emailing_day(date)

    def should_contact(self, person: Person, date: datetime.date) -> bool:
        dt = datetime.datetime.combine(date, datetime.datetime.min.time())
        _, weeknumber, weekday = dt.isocalendar()
        curr_emailing_week = weeknumber % 8
        curr_bucket = weekday + (weeknumber * 8)
        total_days_per_period = 8 * 7
        return (hash(person) % total_days_per_period) == curr_bucket

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

def get_recs(dio_dir: DioDir, schedule: ScheduleABC, date_to_rec: datetime.date) -> Optional[List[Person]]:
    if schedule.should_email_day(date_to_rec):
        should_contact_on_day = functools.partial(
            schedule.should_contact,
            date=date_to_rec
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
            [peep.name for peep in res]
        )

def send_message(contents: str, date: datetime.date, settings: Settings) -> None:
    msg_obj: email.message.EmailMessage = email.message.EmailMessage()
    msg_obj['From'] = settings.smtp_username
    msg_obj['To'] = settings.smtp_dest_email
    msg_obj['Subject'] = "Diogenes | {}".format(str(date))
    msg_obj.set_content(contents)
    with smtplib.SMTP(settings.smtp_url, settings.smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(msg_obj)

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
