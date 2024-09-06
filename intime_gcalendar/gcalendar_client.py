import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .config import Config
from .domain import Event, Lesson, from_dict

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

    def get_events(self, start_date: datetime.datetime, end_date: datetime.datetime) -> list[Event]:
        s, e = start_date.isoformat(), (end_date+datetime.timedelta(days=1)).isoformat()
        res = self.service.events().list(calendarId=self.config.calendar_id,
                                         timeMin=s, timeMax=e, singleEvents=True,
                                         orderBy='startTime').execute().get('items', [])
        return [Event.from_gapi_dict(x) for x in res]

    def add_event(self, event: Event):
        self.service.events().insert(
            calendarId=self.config.calendar_id,
            body=event.to_gapi_dict()).execute()
        
    def update_event(self, id: str, event: Event):
        self.service.events().update(
            calendarId=self.config.calendar_id,
            eventId=id,
            body=event.to_gapi_dict()).execute()
