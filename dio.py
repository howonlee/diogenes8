import os
from typing import Iterator

def is_valid_dir(dir_to_check: str) -> bool:
    parent_dir, filename = os.path.split(dir_to_check)
    if filename.startswith("."):
        return False
    else:
        return os.path.isdir(dir_to_check)

def get_people() -> Iterator[str]:
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    # log curr_dir
    dirs = os.listdir(curr_dir)
    return filter(is_valid_dir, dirs)

if __name__ == "__main__":
    print(list(get_people()))
