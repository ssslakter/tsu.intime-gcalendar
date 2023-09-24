import requests
import json

from data_classes import Faculty, Group, Day

IN_TIME_URL = "https://intime.tsu.ru/api/web/v1"


class InTimeClient:
    def __init__(self):
        pass

    @staticmethod
    def get_faculties() -> list[Faculty]:
        result = requests.get(IN_TIME_URL + "/faculties").json()
        return list(map(lambda x: Faculty(**x), result))

    @staticmethod
    def get_groups(faculty: Faculty):
        result = requests.get(IN_TIME_URL + f"/faculties/{faculty.id}/groups").json()
        return list(map(lambda x: Group.from_dict(x), result))

    @staticmethod
    def get_schedule(group: Group, date_from: str, date_to: str):
        result = requests.get(
            IN_TIME_URL + f"/schedule/group?id={group.id}&dateFrom={date_from}&dateTo={date_to}").json()
        return list(map(lambda x: Day.from_api_dict(x), result))


if __name__ == '__main__':
    client = InTimeClient()
    faculties = client.get_faculties()
    print(faculties)
    groups = client.get_groups(faculties[0])
    print(groups)
    schedule = client.get_schedule(groups[0], "2023-09-04", "2023-09-09")
    print(schedule)
