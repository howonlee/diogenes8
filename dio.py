from __future__ import annotations
import calendar
import os
import json
import random
import datetime
import argparse
import dataclasses
from typing import Iterator, Dict, Any, IO

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
        curr_dir = os.path.abspath(os.path.dirname(__file__))
        dirs = os.listdir(curr_dir)
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
        ######################
        url = "https://api.mailgun.net/v3/{}/messages"\
                .format(settings.mailgun_domain)
        auth = ("api", settings.mailgun_api_key)
        data = self.to_mailgun_data(settings)
        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()
        return response

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
    def get_settings() -> Settings:
        curr_dir = os.path.abspath(os.path.dirname(__file__))
        dio_settings_path = os.path.join(curr_dir, ".dio.json")
        with open(dio_settings_path, "r") as dio_settings_file:
            res = Settings.from_file(dio_settings_file)
        return res


class ScheduleABC(object):
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
###############
###############
###############
###############
        month, weekday = dt.month, dt.weekday
        if month % 3 == 0 and weekday == 7: # sunday
            return True
        return False

    def should_contact(person: Person, dt: datetime.datetime) -> bool:
###############
###############
###############
        person_hash = hash(Person)
        _, num_days_in_month = calendar.monthrange(day.year, day.month)
        return person_hash % num_sundays_in_month == day.day


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
    # mkdir peep_name
    # if exists already, add numbers
    # make Person object, serialize it to a .peep.json file in it
###############
###############
###############
    pass

if __name__ == "__main__":
    argparse.add_argument("subcommand")
    args = argparse.parse_args()
    if args.subcommand == "add":
        add_person(args.name, args.email)
        pass
    elif args.subcommand == "email":
        check_email()
    else:
        raise NotImplementedError("Invalid command")
