import pytz
import click
from data_classes import load_cfg
from gcalendar_client import GCalendarClient
from in_time_client import InTimeClient
from logic import *


def get_group(config):
    faculty = list(filter(lambda x: x.name == config.faculty_name, InTimeClient().get_faculties()))
    if len(faculty) == 0:
        print(f"Faculty '{config.faculty_name}' not found")
        return
    groups = list(filter(lambda x: x.name == config.group_name, InTimeClient().get_groups(faculty[0])))
    if len(groups) == 0:
        print(f"Group '{config.group_name}' not found")
        return
    return groups[0]


def fix_tz(date, config):
    return date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(config.time_zone))


@click.command()
@click.argument("start_date", default=datetime.date.today().strftime("%Y-%m-%d"),
                type=click.DateTime(formats=["%Y-%m-%d"]))
@click.argument("end_date", default=(datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
                type=click.DateTime(formats=["%Y-%m-%d"]))
def main(start_date, end_date):
    config = load_cfg('./config.json')
    start_date, end_date = fix_tz(start_date, config), fix_tz(end_date, config)
    group = get_group(config)
    schedule = InTimeClient().get_schedule(group, start_date, end_date)

    calendar = GCalendarClient(config)
    if config.calendar_id is None:
        config.calendar_id = calendar.create_calendar()
        print(f"calendar id is: {config.calendar_id} \n Please add this to config")

    current_events = calendar.get_events(start_date, end_date)
    schedule += get_custom(start_date, end_date, config)
    for lesson in filter_by_cfg(schedule, config):
        lesson.start = fix_tz(lesson.start, config)
        lesson.end = fix_tz(lesson.end, config)
        print(f"Processing {lesson.start}")
        ev = get_existing_event(current_events, lesson)
        if ev is not None and ev['summary'] == lesson.title:
            print(f"Event {lesson.title} already exists")
            continue
        calendar.add_lesson(lesson, lesson.start)
        print(f"Added {lesson.title}")


if __name__ == '__main__':
    main()
