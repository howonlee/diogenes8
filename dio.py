import os
import json
import datetime
from typing import Iterator, Dict, Any

class Person:
    pass

class Email:
    pass

class Settings:
    pass

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

def filter_people_for_day(
        people: Iterator[Person],
        day: datetime.datetime) -> Iterator[Person]:
###########
###########
###########
###########
    pass

def make_emails(people: Iterator[Person]) -> Iterator[Email]:
###########
###########
###########
###########
###########
    pass

def send_emails(settings: Settings, emails: Iterator[Email]) -> None:
###########
###########
###########
###########
    pass

def get_settings() -> Settings:
    dio_settings_path = os.path.join(get_curr_dir(), ".dio")
    with open(dio_settings_path, "r") as dio_settings_file:
        res = Settings.from_file(dio_settings_file)
    return res

if __name__ == "__main__":
    print(list(get_people()))
