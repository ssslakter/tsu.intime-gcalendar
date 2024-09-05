
from dataclasses import dataclass

from omegaconf import OmegaConf, SCMode

INTIME_URL = "https://intime.tsu.ru/api/web/v1"


@dataclass
class Filters:
    whitelist_groups_names: list[str]
    blacklist_lesson_names: list[str]
    extra_lessons: list[dict]


@dataclass
class Config:
    faculty_name: str
    group_name: str
    filters: Filters
    calendar_id: str
    intime_url: str = INTIME_URL


def load_cfg(file='./config.yaml'):
    conf = OmegaConf.load(file)
    schema = OmegaConf.structured(Config)
    conf: Config = OmegaConf.merge(conf, schema)
    return conf
