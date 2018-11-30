import random
import dataclasses
import os
import os.path
import json
import shutil
from .dio_dir import DioDir
from typing import Dict, List, Any

@dataclasses.dataclass
class Person(object):
    name: str
    salt: str = str(random.randint(int(1e30), int(9e30)))

    def __hash__(self) -> int:
        """
        Don't use a more normal hash dealie, it's not stable between Python instances
        """
        return int(self.salt)

    def to_file(self, person_filename: str) -> None:
        with open(person_filename, "w") as person_file:
            json.dump(dataclasses.asdict(self), person_file)

    def get_dir(self, dio_dir: DioDir) -> str:
        return dio_dir.dirname +\
                "/peep_{}".format(os.path.basename(self.name))

    def save(self, dio_dir: DioDir) -> None:
        """ upserts """
        peep_dirname = self.get_dir(dio_dir)
        if not os.path.exists(peep_dirname):
            os.makedirs(peep_dirname)
        peep_json_filename = Person.get_filename(peep_dirname)
        self.to_file(peep_json_filename)

    def delete(self, dio_dir: DioDir) -> None:
        peep_dirname = self.get_dir(dio_dir)
        if not os.path.exists(peep_dirname):
            raise Exception("Peep directory does not exist to delete")
        else:
            shutil.rmtree(peep_dirname)

    @staticmethod
    def get_filename(dirname: str) -> str:
        return os.path.join(dirname, "peep.json")

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
    def get_all(dio_dir: DioDir) -> List[Person]:
        dio_dir.create_if_not_exists()
        res = []
        for dirpath, _, filenames in os.walk(dio_dir.dirname):
            if "peep_" in dirpath and "peep.json" in filenames:
                res.append(Person.from_dir(dirpath))
        return res


