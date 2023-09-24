import datetime

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


def check_if_lesson_exists(event, lesson: Lesson, date: str):
    return event['summary'] == lesson.title and event['start']['dateTime'] == date + "T" + seconds_to_hms(
        int(lesson.start)) + "+07:00"


def type_to_description(lesson_type: str):
    match lesson_type:
        case "SEMINAR":
            return "Семинар"
        case "LECTURE":
            return "Лекция"
        case "PRACTICE":
            return "Практика"


def seconds_to_hms(seconds: int) -> str:
    return str(datetime.timedelta(seconds=seconds, hours=7))


def filter_by_cfg(lessons: list[Lesson], config: Config) -> list[Lesson]:
    result = []
    for lesson in lessons:
        if lesson.title in config.whitelist_names and lesson.group in config.allowed_group_names:
            result.append(lesson)
    return result
