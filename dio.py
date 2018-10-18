import os

def is_valid_dir(dir_to_check: str) -> bool:
    parent_dir, filename = os.path.split(dir_to_check)
    if filename.startswith("."):
        return False
    else:
        return os.path.isdir(dir_to_check)

if __name__ == "__main__":
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    print(curr_dir)
    dirs = os.listdir(curr_dir)
    for member in dirs:
        member_path = os.path.join(curr_dir, member)
        print(member_path, is_valid_dir(member_path))
    # print(os.listdir(curr_dir))
