import datetime as dt
import inspect
from dataclasses import dataclass
from uuid import uuid4 as guid


def from_dict(cls, d):
    return cls(**{
        k: v for k, v in d.items()
        if k in inspect.signature(cls).parameters
    })


@dataclass
class Faculty:
    id: guid
    name: str


@dataclass
class Group:
    id: guid
    name: str


@dataclass
class Lesson:
    start_utc: dt.datetime
    end_utc: dt.datetime
    title: str
    lesson_type: str = "PRACTICE"
    professor: str = None
    audience: str = None
    groups: str = None

    @staticmethod
    def from_api_dict(date: str, x: dict):
        date = dt.date.fromisoformat(date)
        x['professor'] = x['professor']['fullName']
        x['audience'] = x['audience']['name']
        x['groups'] = ', '.join([g['name'] for g in x['groups']])
        x['start_utc'] = date + dt.timedelta(seconds=x['starts'])
        x['end_utc'] = date + dt.timedelta(seconds=x['ends'])
        return from_dict(Lesson, x)
