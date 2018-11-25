from __future__ import annotations
import calendar
import os
import json
import random
import math
import datetime
import argparse
import dataclasses
import functools
from abc import ABC
from typing import Iterator, Dict, Any, IO, List, Optional

class DioDir(object):
    """
    eventually, un-hard code dio dir from home
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
    name: str
    email: str
    salt: str = str(random.randint(int(1e30), int(9e30)))

    def __hash__(self) -> int:
        return hash("{}_{}_{}".format(
                    self.name,
                    self.email,
                    self.salt))

    def to_file(self, person_file: IO[str]) -> None:
        json.dump(dataclasses.asdict(self), person_file)

    @staticmethod
    def from_file(person_file: IO[str]) -> Person:
        json_res: Dict[str, Any] = json.load(person_file)
        return Person(**json_res)

    @staticmethod
    def from_dir(person_dir: str) -> Person:
        person_filepath = os.path.join(person_dir, ".peep.json")
        with open(person_filepath, "r") as person_file:
            res = Person.from_file(person_file)
        return res

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
        dirs = os.listdir(dio_dir.name)
        peep_dirs = filter(Person.is_peep_dir, dirs)
        return map(Person.from_dir, peep_dirs)


@dataclasses.dataclass
class Recs(object):
    people: List[Person]

    def to_file(self, recs_file: IO[str]) -> None:
        json.dump(dataclasses.asdict(self), recs_file)

    @staticmethod
    def from_file(recs_file: IO[str]) -> Recs:
        json_res: Dict[str, Any] = json.load(recs_file)
        return Recs(**json_res)


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

def get_recs(schedule: ScheduleABC, dt_to_rec: datetime.datetime) -> Optional[Recs]:
    if schedule.should_email_day(dt_to_rec)
        should_contact_on_day = functools.partial(
            schedule.should_contact,
            dt=dt_to_rec
        )
        return Recs(list(filter(should_contact_on_day, Person.get_all())))
    else:
        return None

def add_person(name: str, email: str) -> None:
    # crude hack to prevent dir traversal
    peep_dirname = os.path.expanduser(
            "~/.diogenes/peep_{}".format(os.path.basename(name))
            )
    if not os.path.exists(peep_dirname):
        os.makedirs(peep_dirname)
    new_peep = Person(name, email)
    peep_json_filename = os.path.join(peep_dirname, "peep.json")
    with open(peep_json_filename, "w") as peep_json_file:
        new_peep.to_file(peep_json_file)
    print("added new person: {} with email {}".format(name, email))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand")
    parser.add_argument("--name")
    parser.add_argument("--email")
    args = parser.parse_args()
    dio_dir = DioDir()
    dio_dir.create_if_not_exists()
    if args.subcommand == "add":
        if not args.name:
            raise IOError("Needs a name")
        if not args.email:
            raise IOError("Needs an email")
        add_person(args.name, args.email)
    elif args.subcommand == "recs":
        get_recs()
    else:
        raise NotImplementedError("Invalid command")
