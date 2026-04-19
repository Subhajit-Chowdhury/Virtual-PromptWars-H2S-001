import os
import json
import base64
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

class CalendarHandler:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        self.service = None
        
        raw_creds = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        
        try:
            creds = None
            if raw_creds:
                try:
                    decoded = base64.b64decode(raw_creds).decode('utf-8')
                    info = json.loads(decoded)
                except Exception:
                    clean_json = raw_creds.replace('\\n', '\n').strip()
                    if clean_json.startswith('"') and clean_json.endswith('"'):
                        clean_json = clean_json[1:-1]
                    info = json.loads(clean_json)
                creds = service_account.Credentials.from_service_account_info(info, scopes=self.scopes)
            elif creds_path and os.path.exists(creds_path):
                creds = service_account.Credentials.from_service_account_file(creds_path, scopes=self.scopes)
            
            if creds:
                self.service = build('calendar', 'v3', credentials=creds)
        except Exception as e:
            print(f"Calendar init warning: {e}")
            self.service = None

    def create_reminder(self, summary, description="", start_time_str=None):
        """Creates a calendar event."""
        if not self.service:
            return "Calendar service is not configured. Please check your Google credentials."
        try:
            start_time = datetime.now() + timedelta(hours=1)
            end_time = start_time + timedelta(minutes=30)
            
            event = {
                'summary': f"[DataPulse] {summary}",
                'description': description,
                'start': {
                    'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'timeZone': 'UTC',
                },
            }

            event = self.service.events().insert(calendarId='primary', body=event).execute()
            link = event.get('htmlLink', '')
            return f"[📅 View your new event here]({link})"
        except Exception as e:
            return f"Error creating event: {str(e)}"
