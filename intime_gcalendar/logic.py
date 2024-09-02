import datetime
from typing import Iterable, Iterator

import pytz

from .config import Config
from .models import Lesson


def type_to_color(lesson_type: str):
    """
    blue - 1
    green - 2
    purple - 3
    red - 4
    yellow - 5
    orange - 6
    sky blue - 7
    black - 8
    light blue - 9
    light green - 10
    pink - 11
    """
    match lesson_type:
        case "SEMINAR":
            return "8"
        case "LECTURE":
            return "11"
        case "PRACTICE":
            return "8"
        case "CONTROL_POINT":
            return "3"
        case _:
            return "1"


def get_existing_event(events: list[dict], lesson: Lesson):
    for ev in events:
        start = datetime.datetime.fromisoformat(ev['start']['dateTime'])
        if start == lesson.start_utc:
            return ev
    return None


def type_to_description(lesson_type: str):
    match lesson_type:
        case "SEMINAR":
            return "Семинар"
        case "LECTURE":
            return "Лекция"
        case "PRACTICE":
            return "Практика"
        case "CONTROL_POINT":
            return "Контрольная точка"
        case a:
            return a


def get_custom(start_date: datetime.datetime, end_date: datetime.datetime, config: Config) -> list[Lesson]:
    delta = datetime.timedelta(days=1)
    result = []
    
    for lesson in config.custom:
        date = start_date - delta
        lesson['weekday']-=1
        ls, le = lesson['start'], lesson['end']
        while date <= end_date:
            date += delta
            if date.weekday() != lesson['weekday']:
                continue
            lesson['start'] = read_to_utc(date, ls, config.time_zone)
            lesson['end'] = read_to_utc(date, le, config.time_zone)
            
            result.append(Lesson(**{k:v for k,v in lesson.items() if k!='weekday'}))      
    return result


def read_to_utc(date, time: str, timezone: str):
    tz = pytz.timezone(timezone)
    dt = datetime.datetime.combine(date, time=datetime.time.fromisoformat(time))
    return tz.localize(dt).astimezone(pytz.utc)


def filter_by_cfg(lessons: Iterable[Lesson], config: Config) -> Iterable[Lesson]:
    return _by_group(_by_name(lessons, config), config)


def _by_name(lessons: Iterable[Lesson], config: Config) -> Iterable[Lesson]:
    for lesson in lessons:
        if lesson.title not in config.blacklist:
            yield lesson


def _by_group(lessons: Iterable[Lesson], config: Config) -> Iterable[Lesson]:
    for lesson in lessons:
        if lesson.groups in config.allowed_group_names:
            yield lesson
