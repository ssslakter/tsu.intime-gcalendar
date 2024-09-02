
import json
from dataclasses import dataclass

from intime_gcalendar.in_time_client import INTIME_URL


@dataclass
class Config:
    time_zone: str
    faculty_name: str
    group_name: str
    allowed_group_names: list[str]
    blacklist: list[str]
    custom: list[dict] = None
    calendar_id: str = None
    intime_url: str = INTIME_URL

    @staticmethod
    def load_cfg(file):
        with open(file, 'r', encoding="utf8") as f:
            cfg = json.load(f)
            return Config(**cfg)