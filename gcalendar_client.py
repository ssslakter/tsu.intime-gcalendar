from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from data_classes import Lesson, Config
from logic import type_to_color, type_to_description

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar']


class GCalendarClient:
    def __init__(self, config: Config):
        self.config = config
        self.creds = self.authorize()
        self.service = build('calendar', 'v3', credentials=self.creds)

    @staticmethod
    def authorize():
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds

    def get_colors(self):
        colors = self.service.colors().get().execute()
        for id_, color in colors['event'].items():
            print(f"{id_}: '{color['background']}', '{color['foreground']}'")

    def get_events(self, start_date: datetime.datetime, end_date: datetime.datetime):
        events_result = self.service.events().list(calendarId=self.config.calendar_id, timeMin=start_date.isoformat(),
                                                   timeMax=end_date.isoformat(),
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def create_calendar(self):
        data = {
            'summary': "Schedule",
            'timeZone': self.config.time_zone
        }
        result = self.service.calendars().insert(body=data).execute()
        print(result)
        return result['id']

    def add_lesson(self, lesson: Lesson, date: datetime.datetime):
        event = {
            'summary': lesson.title,
            'location': lesson.audience,
            'description': f"{type_to_description(lesson.lesson_type)}\n{lesson.professor}",
            'start': {
                'dateTime': lesson.start.isoformat()
            },
            'end': {
                'dateTime': lesson.end.isoformat()
            },
            'colorId': type_to_color(lesson.lesson_type),
            'workingLocationProperties.customLocation.label': "lesson"
        }
        self.service.events().insert(calendarId=self.config.calendar_id, body=event).execute()
