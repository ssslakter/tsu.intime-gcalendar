import datetime as dt

import fastcore.all as fc
from fastprogress import progress_bar

from intime_gcalendar.domain import Event, ProcessLessons

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
    pipe = ProcessLessons(config.filters)

    dates = [parse_date(d) for d in [start_date, end_date]]

    group = client.get_group(config.faculty_name, config.group_name).id
    print("Got group number")
    schedule = client.get_schedule(group, *dates)
    print("Got schedule")

    # apply filters
    schedule = list(Event.from_lesson(l) for l in pipe(schedule))
    # schedule += get_custom(start_date, end_date, config)

    current_events = g_client.get_events(*(to_dt(d) for d in dates))
    print("Got current events")
    for ev in schedule:
        if ev in current_events:
            old = current_events[current_events.index(ev)]
            print(f"Updated {old.summary}")
            g_client.update_event(old.id, ev)
        else:
            g_client.add_event(ev)
            print(f"Added {ev.summary}")


if __name__ == '__main__':
    main()
