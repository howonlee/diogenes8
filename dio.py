import os
import json
from typing import Iterator, Dict, Any

def is_valid_dir(dir_to_check: str) -> bool:
    parent_dir, filename = os.path.split(dir_to_check)
    if filename.startswith("."):
        return False
    else:
        return os.path.isdir(dir_to_check)

def get_people() -> Iterator[str]:
    """
    Gets the list of people corresponding to the current
    installation of diogenes
    """
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    # log curr_dir
    dirs = os.listdir(curr_dir)
    return filter(is_valid_dir, dirs)

def get_person(person_dir: str) -> Dict[str, Any]:
    """
    Gets the dictionary representation of a person from
    a str denoting the directory corresponding to the person
    """
    pass

if __name__ == "__main__":
    print(list(get_people()))
