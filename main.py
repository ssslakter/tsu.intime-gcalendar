import click
import datetime
from gcalendar_client import GCalendarClient
from in_time_client import InTimeClient
from logic import *


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")


@click.command()
@click.argument("start_date", default=datetime.date.today().strftime("%Y-%m-%d"),
                type=click.DateTime(formats=["%Y-%m-%d"]))
@click.argument("end_date", default=(datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
                type=click.DateTime(formats=["%Y-%m-%d"]))
def main(start_date, end_date):
    start_date, end_date = str(start_date.date()), str(end_date.date())
    config = Config("1")
    faculty = list(filter(lambda x: x.name == config.faculty_name, InTimeClient().get_faculties()))
    if len(faculty) == 0:
        print(f"Faculty '{config.faculty_name}' not found")
        return
    groups = list(filter(lambda x: x.name == config.group_name, InTimeClient().get_groups(faculty[0])))
    if len(groups) == 0:
        print(f"Group '{config.group_name}' not found")
        return
    schedule = InTimeClient().get_schedule(groups[0], start_date, end_date)

    calendar = GCalendarClient()
    current_events = calendar.get_events(start_date, end_date)
    for day in schedule:
        print(f"Processing {day.date}")
        for lesson in filter_by_cfg(day.lessons, config):
            if any(map(lambda x: check_if_lesson_exists(x, lesson, day.date), current_events)):
                print(f"Event {lesson.title} already exists")
                continue
            calendar.add_lesson(lesson, day.date)
            print(f"Added {lesson.title}")


if __name__ == '__main__':
    main()
