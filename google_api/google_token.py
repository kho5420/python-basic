from __future__ import print_function

import datetime
import os.path
import json
import config
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendar:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        self.file_path = "google_api/token.json"

    def renew_google_token(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.file_path):
            creds = Credentials.from_authorized_user_file(self.file_path, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'google_api/credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.file_path, 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)

    def get_google_token(self):
        self.renew_google_token()

        with open(self.file_path, 'r') as file:
            data = json.load(file)

        return data["token"]

    def get_today_google_calendar(self):
        url = f"https://www.googleapis.com/calendar/v3/calendars/{config.calendar_id}/events"

        now = datetime.datetime.now(datetime.timezone.utc)
        now2 = now + datetime.timedelta(hours=1)

        time_min = now.isoformat()
        time_max = now2.isoformat()

        params = {"key": config.google_api_key, "timeMax": time_max, "timeMin": time_min}
        response = requests.get(url, params=params, headers={"Authorization": f"Bearer {self.get_google_token()}"})

        return response.json()

google_calendar = GoogleCalendar