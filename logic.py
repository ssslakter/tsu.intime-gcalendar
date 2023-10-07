import datetime
from typing import Iterator, Iterable

import pytz

from data_classes import Lesson, Config


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
            return "5"
        case "LECTURE":
            return "2"
        case "PRACTICE":
            return "1"
        case "CONTROL_POINT":
            return "3"
        case _:
            return "1"


def get_existing_event(events: list[dict], lesson: Lesson):
    for ev in events:
        start = datetime.datetime.fromisoformat(ev['start']['dateTime'])
        if start == lesson.start:
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
    date = start_date
    while date <= end_date:
        for lesson in config.custom:
            if date.weekday() != lesson['weekday']:
                continue
            start = read_to_utc(date, lesson['start'], config.time_zone)
            end = read_to_utc(date, lesson['end'], config.time_zone)
            result.append(Lesson(start, end, title=lesson['title']))
        date += delta
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
        if lesson.group in config.allowed_group_names:
            yield lesson
