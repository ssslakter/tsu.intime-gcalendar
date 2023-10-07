import datetime
from dataclasses import dataclass
import json
from uuid import uuid4 as guid
import inspect


# dataclass for faculty
@dataclass
class Faculty:
    id: guid
    name: str


@dataclass
class Group:
    id: guid
    name: str

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass
class Lesson:
    start: datetime.datetime
    end: datetime.datetime
    title: str
    lesson_type: str = "PRACTICE"
    professor: str = None
    audience: str = None
    group: str = None


def from_api_day(day: dict) -> list[Lesson]:
    lessons = filter(lambda x: x["type"] != "EMPTY", day['lessons'])
    date = datetime.datetime.fromisoformat(day['date'])

    def convert(x):
        return Lesson(
            title=x['title'],
            professor=x['professor']['shortName'],
            audience=x['audience']['name'],
            lesson_type=x['lessonType'],
            group=x['groups'][0]['name'],
            start=date + datetime.timedelta(seconds=x['starts']),
            end=date + datetime.timedelta(seconds=x['ends'])
        )

    return [convert(item) for item in lessons]


@dataclass
class Config:
    time_zone: str
    faculty_name: str
    group_name: str
    allowed_group_names: list[str]
    blacklist: list[str]
    custom: list[dict] = None
    calendar_id: str = None


def load_cfg(file):
    with open(file, 'r') as f:
        cfg = json.load(f)
        return Config(**cfg)
