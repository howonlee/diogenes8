from __future__ import annotations
import calendar
import os
import json
import random
import datetime
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

def is_valid_dir(dir_to_check: str) -> bool:
    parent_dir, filename = os.path.split(dir_to_check)
    if filename.startswith("."):
        return False
    else:
        return os.path.isdir(dir_to_check)

def get_curr_dir() -> str:
    return os.path.abspath(os.path.dirname(__file__))

def get_people_dirs() -> Iterator[str]:
    """
    Gets the list of people corresponding to the current
    installation of diogenes
    """
    dirs = os.listdir(get_curr_dir())
    return filter(is_valid_dir, dirs)

def get_people() -> Iterator[Person]:
    return map(get_person, get_people_dirs())

def get_person(person_dir: str) -> Person:
    """
    Gets the dictionary representation of a person from
    a str denoting the directory corresponding to the person
    """
    peep_settings_path = os.path.join(person_dir, ".peep")
    with open(peep_settings_path, "r") as peep_settings_file:
        res = Person.from_file(peep_settings_file)
    return res

def should_email_today(dt: datetime.datetime) -> bool:
    """
    Returns True if we should email ourselves today w/ reminders
    False otherwise
    """
    month = dt.month
    if month % 3 == 0:
        return True
    return False

def should_contact(person: Person, day: datetime.datetime) -> bool:
    person_hash = hash(Person)
    _, num_days_in_month = calendar.monthrange(day.year, day.month)
    return person_hash % num_days_in_month == day.day

def make_email(person: Person) -> Email:
    subject: str = f"[Diogenes] Contact {person.name}"
    text: str = f"It's time to contact {person.name}. Email is {person.email}"
    return Email(dest_addr=person.email,
                 subject=subject,
                 text=text)

def send_email(settings: Settings, email: Email) -> None:
##################
##################
##################
##################
    url = "some shit".format(settings.mailgun_domain)
    auth = ("api", settings.mailgun_api_key)
    data = email.to_mailgun_data(settings)
    response = requests.post(url, auth=auth, data=data)
    response.raise_for_status()

def get_settings() -> Settings:
    dio_settings_path = os.path.join(get_curr_dir(), ".dio")
    with open(dio_settings_path, "r") as dio_settings_file:
        res = Settings.from_file(dio_settings_file)
    return res

def main() -> None:
############
############
############
############
############
    pass

if __name__ == "__main__":
    main()
    print(list(get_people()))
