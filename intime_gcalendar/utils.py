import datetime as dt



def parse_date(date): return dt.date.fromisoformat(date)


def date_with_seconds(date: dt.date, seconds: int, tzinfo=dt.timezone.utc) -> dt.datetime:
    return dt.datetime.combine(date, dt.time(), tzinfo) + dt.timedelta(seconds=seconds)

def to_dt(date: dt.date): return date_with_seconds(date, 0)

