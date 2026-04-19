import os
import json
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build

class SheetsHandler:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')
        
        raw_creds = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        self.creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        
        if raw_creds:
            try:
                # 1. Try decoding as Base64 (The most reliable cloud method)
                try:
                    decoded = base64.b64decode(raw_creds).decode('utf-8')
                    info = json.loads(decoded)
                except Exception:
                    # 2. Fallback: Treat as raw JSON and fix common formatting issues
                    clean_json = raw_creds.replace('\\n', '\n').strip()
                    if clean_json.startswith('"') and clean_json.endswith('"'):
                        clean_json = clean_json[1:-1]
                    info = json.loads(clean_json)
                
                self.creds = service_account.Credentials.from_service_account_info(
                    info, scopes=self.scopes)
            except Exception as e:
                raise ValueError(f"CRITICAL: Failed to parse GOOGLE_SERVICE_ACCOUNT_JSON. Detail: {str(e)}")
        elif self.creds_path and os.path.exists(self.creds_path):
            self.creds = service_account.Credentials.from_service_account_file(
                self.creds_path, scopes=self.scopes)
        else:
            raise FileNotFoundError("No Google credentials found")
            
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
