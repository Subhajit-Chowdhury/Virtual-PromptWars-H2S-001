import os
import json
import base64
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

class CalendarHandler:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        
        raw_creds = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        self.creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        
        if raw_creds:
            try:
                try:
                    # 1. Try Base64
                    decoded = base64.b64decode(raw_creds).decode('utf-8')
                    info = json.loads(decoded)
                except Exception:
                    # 2. Fallback
                    clean_json = raw_creds.replace('\\n', '\n').strip()
                    if clean_json.startswith('"') and clean_json.endswith('"'):
                        clean_json = clean_json[1:-1]
                    info = json.loads(clean_json)
                
                self.creds = service_account.Credentials.from_service_account_info(
                    info, scopes=self.scopes)
            except Exception as e:
                print(f"Calendar Credential Error: {e}")
                raise ValueError("Failed to load Calendar credentials")
        elif self.creds_path and os.path.exists(self.creds_path):
            self.creds = service_account.Credentials.from_service_account_file(
                self.creds_path, scopes=self.scopes)
        else:
            raise FileNotFoundError("No Google credentials found")
            
        self.service = build('calendar', 'v3', credentials=self.creds)

    def create_reminder(self, summary, description="", start_time_str=None):
        """Creates a calendar event."""
        try:
            if not start_time_str:
                start_time = datetime.now() + timedelta(hours=1)
            else:
                start_time = datetime.now() + timedelta(hours=1)
                
            end_time = start_time + timedelta(minutes=30)
            
            event = {
                'summary': f"[Data Assistant] {summary}",
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
            return f"Event created: {event.get('htmlLink')}"
        except Exception as e:
            return f"Error accessing Calendar: {str(e)}"
