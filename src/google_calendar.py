import datetime
import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GoogleCalendar:

    def __init__(self):
        self.creds = None
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']

        if os.path.exists('config/token.json'):
            with open('config/token.json', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'config/credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('config/token.json', 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def schedule_event(self, event_details):
        event = {
            'summary': event_details['summary'],
            'start': {
                'dateTime': event_details['start_time'],
                'timeZone': 'America/New_York',
            },
        }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))