import datetime as dt
import inspect
from dataclasses import dataclass
from typing import Iterable
from uuid import uuid4 as guid

from .config import Filters
from .utils import date_with_seconds


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
    starts_utc: dt.datetime
    ends_utc: dt.datetime
    title: str
    lesson_type: str
    professor: str = None
    audience: str = None
    groups: str = None

    @staticmethod
    def from_api_dict(date: str, x: dict):
        date = dt.date.fromisoformat(date)
        x['professor'] = x['professor']['fullName']
        x['audience'] = x['audience']['name']
        x['groups'] = ', '.join([g['name'] for g in x['groups']])
        x['lesson_type'] = x['lessonType']
        for k in ['starts', 'ends']:
            # api uses seconds from midnight in UTC
            x[f'{k}_utc'] = date_with_seconds(date, x[k], tzinfo=dt.timezone.utc)
        return from_dict(Lesson, x)


@dataclass
class Event:
    '''Google calendar event'''
    summary: str
    start: dt.datetime
    end: dt.datetime
    location: str = None
    description: str = None
    id: str = None
    
    def __eq__(self, other):
        # we want to compare only by summary, start and end, for cases when description or location changes
        return all(getattr(self, k) == getattr(other, k) for k in ['summary', 'start', 'end'])
    
    @staticmethod
    def from_lesson(lesson: Lesson):
        return Event(
            summary=lesson.title,
            location=lesson.audience,
            description=f"{type_to_desc(lesson.lesson_type)}\n{lesson.professor}\n{lesson.groups}",
            start=lesson.starts_utc,
            end=lesson.ends_utc
        )
        
    @staticmethod
    def from_gapi_dict(d):
        for k in ['start', 'end']:
            d[k] = dt.datetime.fromisoformat(d[k]['dateTime'])
        return from_dict(Event, d)
    
    def to_gapi_dict(self):
        return {
            'summary': self.summary,
            'location': self.location,
            'description': self.description,
            'start': {'dateTime': self.start.isoformat()},
            'end': {'dateTime': self.end.isoformat()}
        }

def type_to_desc(lesson_type: str):
    dm = {
        "SEMINAR": "Семинар",
        "LECTURE": "Лекция",
        "PRACTICE": "Практика",
        "CONTROL_POINT": "Контрольная точка",
    }
    return dm.get(lesson_type, lesson_type)


class ProcessLessons:
    def __init__(self, filters: Filters):
        self.filters = filters

    def __call__(self, lessons: Iterable[Lesson]):
        '''Process lessons according to config'''
        return self.filter_names(
            self.filter_groups(lessons, self.filters.whitelist_groups_names),
            self.filters.blacklist_lesson_names)

    @staticmethod
    def filter_names(lessons: Iterable[Lesson], names: list[str], whitelist=False) -> Iterable[Lesson]:
        p = (lambda x: x in names) if whitelist else lambda x: x not in names
        return (l for l in lessons if p(l.title))

    @staticmethod
    def filter_groups(lessons: Iterable[Lesson], groups: list[str], whitelist=True) -> Iterable[Lesson]:
        p = (lambda x: x in groups) if whitelist else lambda x: x not in groups
        return (l for l in lessons if p(l.groups))
