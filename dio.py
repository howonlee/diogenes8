import os
import json
import datetime
from typing import Iterator, Dict, Any

def is_valid_dir(dir_to_check: str) -> bool:
    parent_dir, filename = os.path.split(dir_to_check)
    if filename.startswith("."):
        return False
    else:
        return os.path.isdir(dir_to_check)

def get_curr_dir() -> str:
    return os.path.abspath(os.path.dirname(__file__))

def get_people_list() -> Iterator[str]:
    """
    Gets the list of people corresponding to the current
    installation of diogenes
    """
    dirs = os.listdir(get_curr_dir())
    return filter(is_valid_dir, dirs)

def get_people() -> Iterator[Dict[str, Any]]:
    return map(get_person, get_people_list())

def get_person(person_dir: str) -> Dict[str, Any]:
    """
    Gets the dictionary representation of a person from
    a str denoting the directory corresponding to the person
    """
    peep_settings_path = os.path.join(person_dir, ".peep")
    with open(peep_settings_path, "r") as peep_settings_file:
        res = json.load(peep_settings_file)
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
        people: Iterator[Dict[str, Any]],
        day: datetime.datetime) -> Iterator[Dict[str, Any]]:
    """
    Returns True if we should email ourselves today w/ reminders
    False otherwise
    """
###########
###########
###########
###########
    pass

def make_emails(people: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, str]]:
###########
###########
###########
###########
###########
    pass

def send_emails(settings: Dict[str, Any], emails: iterator[Dict[str, str]]) -> None:
###########
###########
###########
###########
    pass

def get_settings() -> Dict[str, Any]:
    dio_settings_path = os.path.join(get_curr_dir(), ".dio")
    with open(dio_settings_path, "r") as dio_settings_file:
        res = json.load(dio_settings_file)
    return res

if __name__ == "__main__":
    print(list(get_people()))
