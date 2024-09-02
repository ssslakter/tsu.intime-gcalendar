import datetime as dt

import requests

from .models import Faculty, Group, Lesson, from_dict

INTIME_URL = "https://intime.tsu.ru/api/web/v1"


class InTimeClient:
    def __init__(self, api_url=INTIME_URL):
        self.api_url = api_url

    def get(self, path: str, cls: type):
        res = requests.get(f"{self.api_url}{path}").json()
        return [from_dict(cls, f) for f in res]

    def get_faculties(self, substr: str) -> list[Faculty]:
        res = self.get("/faculties", Faculty)
        return [f for f in res if substr.lower() in f.name.lower()]

    def get_groups(self, faculty: Faculty, substr: str) -> list[Group]:
        res = self.get(f"/faculties/{faculty.id}/groups", Group)
        return [g for g in res if substr.lower() in g.name.lower()]

    def get_schedule(self, group_id: Group, start_date: dt.date, end_date: dt.date) -> list[Lesson]:
        res = requests.get(f"{self.api_url}/schedule/group?id={group_id}&dateFrom={start_date}&dateTo={end_date}").json()

        return [Lesson.from_api_dict(day['date'], lesson)
                for day in res['grid']
                for lesson in day['lessons'] 
                if lesson['type'] != "EMPTY"]

    def get_group(self, faculty_name, group_name):
        if fs := self.get_faculties(faculty_name):
            if gs := self.get_groups(fs[0], group_name):
                return gs[0]
            raise LookupError(f"Group '{group_name}' not found")
        else: raise LookupError(f"Faculty '{faculty_name}' not found")
