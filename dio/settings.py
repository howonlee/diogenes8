import dataclasses
import json
from typing import Dict, Any

@dataclasses.dataclass
class Settings(object):
    smtp_username: str
    smtp_password: str
    smtp_dest_email: str
    smtp_url: str = "smtp.gmail.com"
    smtp_port: int = 587

    def to_file(self, settings_filename: str) -> None:
        with open(settings_filename, "w") as settings_file:
            json.dump(dataclasses.asdict(self), settings_file)

    @staticmethod
    def from_file(settings_filename: str) -> Settings:
        with open(settings_filename, "r") as settings_file:
            json_res: Dict[str, Any] = json.load(settings_file)
            return Settings(**json_res)
