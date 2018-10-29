from __future__ import annotations
import calendar
import os
import json
import random
import math
import datetime
import argparse
import dataclasses
from abc import ABC
from typing import Iterator, Dict, Any, IO

class DioDir(object):
    """
    eventually, un-hard code dio dir from home
    """
    pass

@dataclasses.dataclass
class Person(object):
    email: str
    name: str
    salt: str = str(random.randint(1e30, 9e30))

    def __hash__(self) -> long:
        return hash("{}_{}_{}".format(
                    self.email,
                    self.name,
                    self.salt))

    def to_file(person_file: IO[str]) -> None:
        json.dump(dataclasses.asdict(self), person_file)

    @staticmethod
    def from_file(person_file: IO[str]) -> Person:
        json_res: Dict[str, Any] = json.load(person_file)
        return self.__init__(**json_res)

    @staticmethod
    def from_dir(person_dir: str) -> Person:
        peep_settings_path = os.path.join(person_dir, ".peep.json")
        with open(peep_settings_path, "r") as peep_settings_file:
            res = Person.from_file(peep_settings_file)
        return res

    @staticmethod
    def is_peep_dir(dir_to_check: str) -> bool:
        parent_dir, filename = os.path.split(dir_to_check)
        if filename.startswith("peep_"):
            return os.path.isdir(dir_to_check)
        else:
            return False

    @staticmethod
    def get_all() -> Iterator[Person]:
        create_dio_dir_if_not_exists()
        dio_dir = os.path.expanduser("~/.diogenes")
        dirs = os.listdir(dio_dir)
        peep_dirs = filter(is_peep_dir, dirs)
        return map(Person.from_dir, peep_dirs)


@dataclasses.dataclass
class Email(object):
    dest_addr: str
    subject: str
    text: str

    def to_mailgun_data(self, settings: Settings):
        return {
            "from": "Diogenes <mailgun@{}>".format(settings.mailgun_domain),
            "to": self.dest_addr,
            "subject": self.subject,
            "text": self.text,
        }

    def send(self, settings: Settings) -> requests.Response:
        ######################
        ###################### de-hard-code the url to make testable
        ###################### later todo would be to de-hard-code from mailgun, but we're going w/ mailgun for now
        ######################
        url = "https://api.mailgun.net/v3/{}/messages"\
                .format(settings.mailgun_domain)
        auth = ("api", settings.mailgun_api_key)
        data = self.to_mailgun_data(settings)
        print(data)
        return None
        # response = requests.post(url, auth=auth, data=data)
        # response.raise_for_status()
        # return response

    @staticmethod
    def from_person(person: Person) -> Email:
        subject: str = f"[Diogenes] Contact {person.name}"
        text: str = f"It's time to contact {person.name}. Email is {person.email}"
        return Email(dest_addr=person.email,
                     subject=subject,
                     text=text)


@dataclasses.dataclass
class Settings(object):
    mailgun_domain: str
    mailgun_api_key: str

    def to_file(settings_file: IO[str]) -> None:
        json.dump(dataclasses.asdict(self), settings_file)

    @staticmethod
    def from_file(settings_file: IO[str]) -> Settings:
        json_res: Dict[str, Any] = json.load(settings_file)
        return self.__init__(**json_res)

    @staticmethod
    def create_settings_if_not_exists(dio_dir: str) -> None:
        default_settings = Settings(mailgun_domain="",
                                    mailgun_api_key="")
        with open(os.path.join(dio_dir, ".dio.json"), "w") as settings_file:
            default_settings.to_file(settings_file)

    @staticmethod
    def get_settings() -> Settings:
        create_dio_dir_if_not_exists()
        dio_dir = os.path.expanduser("~/.diogenes")
        create_settings_if_not_exists(dio_dir)
        dio_settings_path = os.path.join(dio_dir, ".dio.json")
        with open(dio_settings_path, "r") as dio_settings_file:
            res = Settings.from_file(dio_settings_file)
        return res


class ScheduleABC(ABC):
    def __init__(self):
        pass

    def should_email_day(dt: datetime.datetime) -> bool:
        """
        Returns True if we should email ourselves on day w/ reminders
        False otherwise
        """
        raise NotImplementedError()

    def should_contact(person: Person, dt: datetime.datetime) -> bool:
        raise NotImplementedError()

class DefaultSchedule(ScheduleABC):
    def __init__(self):
        pass

    def should_email_day(dt: datetime.datetime) -> bool:
        # isocalendar has Monday 1 and Sunday 7
        # we want every 2nd Saturday
        _, weeknumber, weekday = dt.isocalendar()
        if weeknumber % 2 == 0 and weekday == 6:
            return True
        return False

    def should_contact(person: Person, dt: datetime.datetime) -> bool:
        # 28 Dec is always in last week of year
        num_weeks_in_year = datetime.date(dt.year, 12, 28)\
                .isocalendar()[1]
        _, weeknumber, weekday = dt.isocalendar()
        person_hash = hash(Person)
        rounded_weeknumber = int(math.ceil(weeknumber / 2.) * 2)
        return (person_hash % num_weeks_in_year) == rounded_weeknumber

def check_email() -> None:
    if should_email_day(datetime.datetime.today()):
        curr_settings = Settings.get_settings()
        for person in get_people():
            if should_contact(person, datetime.datetime.today()):
                curr_email = Email.from_person(person)
                curr_email.send(curr_settings)
    else:
        pass

def add_person(name: str, email: str) -> None:
##############
##############
##############
##############
    peep_dirname = NotImplemented() ############
    # mkdir peep_name
    # if exists already, add numbers
    if not os.path.exists(dio_dirname):
        os.makedirs(dio_dirname)
    else:
        os.makedirs(dio_dirname + NotImplemented)
    new_peep = Person(NotImplemented)
    peep_json_filename = NotImplemented
    with open(peep_json_filename, "w") as peep_json_file:
        new_peep.to_file(peep_json_file)

def create_dio_dir_if_not_exists() -> None:
    """ Not threadsafe but otherwise idempotent """
    dio_dirname = os.path.expanduser("~/.diogenes")
    if not os.path.exists(dio_dirname):
        os.makedirs(dio_dirname)

if __name__ == "__main__":
    create_dio_dir_if_not_exists()
    argparse.add_argument("subcommand")
    args = argparse.parse_args()
    if args.subcommand == "add":
        add_person(args.name, args.email)
        pass
    elif args.subcommand == "email":
        check_email()
    else:
        raise NotImplementedError("Invalid command")
