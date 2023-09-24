from dataclasses import dataclass, field
from uuid import uuid4 as guid
import inspect


# dataclass for faculty
@dataclass
class Faculty:
    id: guid
    name: str


@dataclass
class Group:
    id: guid
    name: str

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass
class Lesson:
    lesson_type: str
    title: str
    professor: str
    start: str
    end: str
    audience: str
    group: str

    @classmethod
    def from_api_dict(cls, env):
        return cls(**{'title': env['title'],
                      'professor': env['professor']['shortName'],
                      'start': env['starts'],
                      'end': env['ends'],
                      'audience': env['audience']['name'],
                      'lesson_type': env['lessonType'],
                      'group': env['groups'][0]['name']
                      })


@dataclass
class Day:
    date: str
    lessons: list[Lesson]

    @classmethod
    def from_api_dict(cls, env):
        lessons = filter(lambda x: x["type"] != "EMPTY", env['lessons'])
        return cls(**{
            "date": env['date'],
            "lessons": list(map(lambda x: Lesson.from_api_dict(x), lessons))
        })


@dataclass
class Config:
    calendar_id: str
    faculty_name: str = field(default='Научно-образовательный центр "Высшая ИТ школа"')
    group_name: str = field(default="972103")
    allowed_group_names: list[str] = field(
        default_factory=lambda: ['972103', '972103 (1)', '972103 (М2)'])
    whitelist_names: list[str] = field(
        default_factory=lambda: ['Философия',
                                 'Профессиональный английский язык',
                                 'Прикладная статистика',
                                 'Паттерны архитектуры 1',
                                 'Наукоемкая разработка 1',
                                 'Семинар по специализации М2'])
