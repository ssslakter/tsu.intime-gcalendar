import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .config import Config
from .domain import Lesson

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
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_events(self, start_date: datetime.datetime, end_date: datetime.datetime):
        events_result = self.service.events().list(calendarId=self.config.calendar_id, timeMin=start_date,
                                                   timeMax=end_date+datetime.timedelta(days=1),
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    def create_calendar(self):
        result = self.service.calendars().insert(body={'summary': "Schedule"}).execute()
        return result['id']

    def add_lesson(self, lesson: Lesson, date: datetime.datetime):
        event = {
            'summary': lesson.title,
            'location': lesson.audience,
            'description': f"{type_to_description(lesson.lesson_type)}\n{lesson.professor}",
            'start': {
                'dateTime': lesson.start_utc.isoformat()+"Z"
            },
            'end': {
                'dateTime': lesson.end_utc.isoformat()+"Z"
            },
            'workingLocationProperties.customLocation.label': "lesson"
        }
        self.service.events().insert(calendarId=self.config.calendar_id, body=event).execute()
