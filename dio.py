from __future__ import annotations
import calendar
import os
import shutil
import json
import random
import math
import marshmallow
import datetime
import argparse
import dataclasses
import functools
from abc import ABC
from typing import Iterator, Dict, Any, IO, List, Optional

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
        self.settings_file = os.path.join(self.dirname, "settings.json")

    def create_settings_if_not_exists(self):
        default_schema = {
        }
        ###########
        ########### settings should basically have a json schema
        ###########
        raise NotImplementedError()

    def get_settings(self):
        self.create_settings_if_not_exists()
        pass

    def create_if_not_exists(self):
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

@dataclasses.dataclass
class Person(object):
    """
    We want a general data object, really
    """
    def __init__(self, name: str, email: str, salt: Optional[str]):
        self.name = name
        self.email = email
        if not salt:
            self.salt = str(random.randint(int(1e30), int(9e30)))
        else:
            self.salt = salt

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

    def create(self, dio_dir: DioDir) -> None:
        peep_dirname = self.get_dir(dio_dir)
        if not os.path.exists(peep_dirname):
            os.makedirs(peep_dirname)
        peep_json_filename = Person.get_filename(peep_dirname)
        self.to_file(peep_json_filename)

    def remove(self, dio_dir: DioDir) -> None:
        peep_dirname = self.get_dir(dio_dir)
        if not os.path.exists(peep_dirname):
            raise Exception("Peep directory does not exist to remove")
        else:
            shutil.rmtree(peep_dirname)

    @staticmethod
    def get_filename(dirname: str) -> str:
        return os.path.join(dirname, ".peep.json")

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
        if filename.startswith("peep_"):
            return os.path.isdir(dir_to_check)
        else:
            return False

    @staticmethod
    def get_all(dio_dir: DioDir) -> Iterator[Person]:
        dio_dir.create_if_not_exists()
        dirs = os.listdir(dio_dir.dirname)
        peep_dirs = filter(Person.is_peep_dir, dirs)
        return map(Person.from_dir, peep_dirs)


class ScheduleABC(ABC):
    def __init__(self):
        pass

    def should_email_day(self, dt: datetime.datetime) -> bool:
        """
        Returns True if we should email ourselves on day w/ reminders
        False otherwise
        """
        raise NotImplementedError()

    def should_contact(self, person: Person, dt: datetime.datetime) -> bool:
        raise NotImplementedError()


class DefaultSchedule(ScheduleABC):
    def __init__(self):
        pass

    def should_email_day(self, dt: datetime.datetime) -> bool:
        # isocalendar has Monday 1 and Sunday 7
        # we want every 2nd Saturday
        _, weeknumber, weekday = dt.isocalendar()
        if weeknumber % 2 == 0 and weekday == 6:
            return True
        return False

    def should_contact(self, person: Person, dt: datetime.datetime) -> bool:
        # 28 Dec is always in last week of year
        num_weeks_in_year = datetime.date(dt.year, 12, 28)\
                .isocalendar()[1]
        _, weeknumber, weekday = dt.isocalendar()
        person_hash = hash(Person)
        rounded_weeknumber = int(math.ceil(weeknumber / 2.) * 2)
        return (person_hash % num_weeks_in_year) == rounded_weeknumber

def get_recs(dio_dir: DioDir, schedule: ScheduleABC, dt_to_rec: datetime.datetime) -> Optional[List[Person]]:
    if schedule.should_email_day(dt_to_rec):
        should_contact_on_day = functools.partial(
            schedule.should_contact,
            dt=dt_to_rec
        )
        return list(filter(should_contact_on_day, Person.get_all(dio_dir)))
    else:
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand")
    parser.add_argument("--name")
    args = parser.parse_args()
    dio_dir = DioDir()
    dio_dir.create_if_not_exists()
    today = datetime.datetime.now()
    sched = DefaultSchedule()
    if args.subcommand == "add":
        if not args.name:
            raise IOError("Needs a name")
        if not args.email:
            raise IOError("Needs an email")
        new_peep = Person(name=args.name)
        new_peep.create(dio_dir)
    elif args.subcommand == "recs":
        get_recs(dio_dir, sched, today)
    else:
        raise NotImplementedError("Invalid command")
