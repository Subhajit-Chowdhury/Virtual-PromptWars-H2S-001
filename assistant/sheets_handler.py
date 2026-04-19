import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

class SheetsHandler:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')
        
        # Production Secret Management: Support both file-based and ENV-based credentials
        creds_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        self.creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        
        if creds_json:
            # Load directly from ENV (Best for Vercel/Cloud)
            info = json.loads(creds_json)
            self.creds = service_account.Credentials.from_service_account_info(
                info, scopes=self.scopes)
        elif self.creds_path and os.path.exists(self.creds_path):
            # Load from file (Best for Local)
            self.creds = service_account.Credentials.from_service_account_file(
                self.creds_path, scopes=self.scopes)
        else:
            raise FileNotFoundError("No Google credentials found (Check GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_CREDENTIALS_PATH)")
            
        self.service = build('sheets', 'v4', credentials=self.creds)

    def validate_data(self, values):
        """Production-grade data quality check (Nulls, Duplicates)."""
        if not values or len(values) < 2:
            return "DATA_ERROR: Empty or insufficient data."
        
        headers = values[0]
        rows = values[1:]
        
        report = []
        null_count = 0
        duplicate_count = 0
        seen_rows = set()
        
        for row in rows:
            if any(not str(cell).strip() for cell in row):
                null_count += 1
            
            row_tuple = tuple(row)
            if row_tuple in seen_rows:
                duplicate_count += 1
            seen_rows.add(row_tuple)
            
        if null_count > 0:
            report.append(f"QUALITY_ALERT: Found {null_count} rows with empty values.")
        if duplicate_count > 0:
            report.append(f"QUALITY_ALERT: Found {duplicate_count} duplicate rows.")
            
        return " | ".join(report) if report else "DATA_QUALITY: High Integrity (0 errors detected)."

    def get_sheet_data(self):
        """Fetches and validates data from the first tab of the spreadsheet."""
        try:
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
            sheet_name = spreadsheet['sheets'][0]['properties']['title']
            
            range_name = f"{sheet_name}!A1:H100"
            result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                        range=range_name).execute()
            values = result.get('values', [])
            
            if not values:
                return "No data found."
            
            quality_report = self.validate_data(values)
            data_str = f"QUALITY_REPORT: {quality_report}\n\n"
            headers = values[0]
            for row in values[1:]:
                padded_row = row + [""] * (len(headers) - len(row))
                row_data = [f"{headers[i]}: {padded_row[i]}" for i in range(len(headers))]
                data_str += " | ".join(row_data) + "\n"
            
            return data_str
        except Exception as e:
            return f"Error accessing Sheets: {str(e)}"
