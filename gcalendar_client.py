from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from data_classes import Lesson
from logic import type_to_color, seconds_to_hms, type_to_description

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/calendar.readonly']


class GCalendarClient:
    def __init__(self):
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

    def get_events(self, start_date: str, end_date: str):
        events_result = self.service.events().list(calendarId='primary', timeMin=start_date + "T00:00:00+07:00",
                                                   timeMax=end_date + "T00:00:00+07:00",
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def add_lesson(self, lesson: Lesson, date: str):
        event = {
            'summary': lesson.title,
            'location': lesson.audience,
            'description': f"{type_to_description(lesson.lesson_type)}\n{lesson.professor}",
            'start': {
                'dateTime': date + "T" + seconds_to_hms(int(lesson.start)) + "+07:00"
            },
            'end': {
                'dateTime': date + "T" + seconds_to_hms(int(lesson.end)) + "+07:00"
            },
            'colorId': type_to_color(lesson.lesson_type),
            'workingLocationProperties.customLocation.label': "lesson"
        }
        self.service.events().insert(calendarId='primary', body=event).execute()
