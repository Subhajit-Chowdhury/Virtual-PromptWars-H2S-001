import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

class SheetsHandler:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')
        
        if not self.creds_path or not os.path.exists(self.creds_path):
            raise FileNotFoundError(f"Service account file not found: {self.creds_path}")
            
        self.creds = service_account.Credentials.from_service_account_file(
            self.creds_path, scopes=self.scopes)
        self.service = build('sheets', 'v4', credentials=self.creds)

    def get_sheet_data(self, range_name='SalesData!A1:H100'):
        """Fetches data from the spreadsheet."""
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                        range=range_name).execute()
            values = result.get('values', [])
            
            if not values:
                return "No data found."
            
            # Convert to a simple string representation for the AI to read
            data_str = ""
            headers = values[0]
            for row in values[1:]:
                row_data = [f"{headers[i]}: {row[i]}" for i in range(len(row))]
                data_str += " | ".join(row_data) + "\n"
            
            return data_str
        except Exception as e:
            return f"Error accessing Sheets: {str(e)}"
