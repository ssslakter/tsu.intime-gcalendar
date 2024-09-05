import datetime as dt

import fastcore.all as fc

from .config import load_cfg
from .gcalendar_client import GCalendarClient
from .in_time_client import InTimeClient
from .utils import *

today = dt.date.today()


@fc.call_parse
def main(
    start_date: str = str(today),
    end_date: str = str(today+dt.timedelta(days=7))
):
    config = load_cfg()
    client = InTimeClient(config.intime_url)
    g_client = GCalendarClient(config)
    
    dates = [parse_date(d) for d in [start_date, end_date]]
    
    schedule = client.get_schedule(
        client.get_group(config.faculty_name, config.group_name).id,
        *dates)
    
    if config.calendar_id is None:
        config.calendar_id = g_client.create_calendar()
        print(f"calendar id is: {config.calendar_id} \n Please add this to the config")

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
