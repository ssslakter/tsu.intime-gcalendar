import datetime as dt

import fastcore.all as fc
import pytz
from .logic import *

from .config import Config
from .gcalendar_client import GCalendarClient
from .in_time_client import InTimeClient


# def fix_tz(date, config):
#     return date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(config.time_zone))

def to_dt(date):# -> Any:
    return dt.datetime.combine(date, dt.datetime.min.time())

def parse_date(date):
    return dt.date.fromisoformat(date)

today = dt.date.today()


@fc.call_parse
def main(
    start_date: str = str(today),
    end_date: str = str(today+dt.timedelta(days=7))
):
    config = Config.load_cfg('./config.json')
    client = InTimeClient(config.intime_url)

    start_date, end_date = parse_date(start_date), parse_date(end_date)
    group = client.get_group(config.faculty_name, config.group_name)
    schedule = client.get_schedule(group.id, start_date, end_date)
    
    g_client = GCalendarClient(config)
    if config.calendar_id is None:
        config.calendar_id = g_client.create_calendar()
        print(f"calendar id is: {config.calendar_id} \n Please add this to config")

    current_events = g_client.get_events(to_dt(start_date), to_dt(end_date))
    schedule += get_custom(start_date, end_date, config)
    for lesson in filter_by_cfg(schedule, config):
        # lesson.start_utc = fix_tz(lesson.start_utc, config)
        # lesson.end_utc = fix_tz(lesson.end_utc, config)
        print(f"Processing {lesson.start_utc}")
        ev = get_existing_event(current_events, lesson)
        if ev is not None and ev['summary'] == lesson.title:
            print(f"Event {lesson.title} already exists")
            continue
        # g_client.add_lesson(lesson, lesson.start_utc)
        print(f"Added {lesson.title}")


if __name__ == '__main__':
    main()
