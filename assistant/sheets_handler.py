import os
import json
import base64
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

class SheetsHandler:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        self.credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        self.creds = self._load_credentials()
        self.service = build('sheets', 'v4', credentials=self.creds) if self.creds else None

    def _load_credentials(self):
        try:
            # 1. Try loading from Base64 (Production/Vercel strategy)
            if self.service_account_json:
                decoded_json = base64.b64decode(self.service_account_json).decode('utf-8')
                creds_info = json.loads(decoded_json)
                return service_account.Credentials.from_service_account_info(creds_info, scopes=self.scopes)

            # 2. Try loading from local file (Local dev strategy)
            if self.credentials_path and os.path.exists(self.credentials_path):
                return service_account.Credentials.from_service_account_file(self.credentials_path, scopes=self.scopes)
        except Exception as e:
            print(f"Warning: Failed to load Google credentials: {e}")
        return None

    def get_sheet_data(self, spreadsheet_id):
        if not self.service:
            return "Google Sheets service not initialized. Please check credentials.", {}
        try:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', '')
            if not sheets:
                return "No sheets found in spreadsheet.", {}
            
            first_sheet_name = sheets[0].get("properties", {}).get("title", "Sheet1")
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, 
                range=f"'{first_sheet_name}'!A1:Z100"
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return "Empty spreadsheet.", {}

            df = pd.DataFrame(values[1:], columns=values[0])
            cleaned_df, audit_report = self.validate_data(df)
            return cleaned_df.to_string(index=False), audit_report
        except Exception as e:
            return f"Error accessing Sheets: {str(e)}", {}

    def get_local_data(self, file_path):
        """
        Parses an uploaded CSV, XLSX, or JSON file and returns cleaned data + audit report.
        """
        try:
            ext = file_path.split('.')[-1].lower()
            if ext == 'csv':
                df = pd.read_csv(file_path)
            elif ext == 'xlsx':
                df = pd.read_excel(file_path)
            elif ext == 'json':
                df = pd.read_json(file_path)
            else:
                return f"Unsupported file format: {ext}", {}

            cleaned_df, audit_report = self.validate_data(df)
            return cleaned_df.to_string(index=False), audit_report
        except Exception as e:
            return f"Error reading file: {str(e)}", {}

    def validate_data(self, df):
        """
        Performs a data integrity audit on the provided dataframe.
        """
        # Ensure we have strings for comparison if it's a mix
        df = df.astype(str)
        initial_row_count = len(df)
        
        # 1. Detect Duplicates
        duplicate_count = df.duplicated().sum()
        df_no_dupes = df.drop_duplicates()
        
        # 2. Detect Nulls (inc empty strings)
        null_count = df_no_dupes.isnull().sum().sum() + (df_no_dupes == "").sum().sum() + (df_no_dupes == "nan").sum().sum()
        
        # Fill nulls with 'N/A'
        final_df = df_no_dupes.replace({"": "N/A", "nan": "N/A"}).fillna("N/A")
        
        audit_report = {
            "rows_checked": initial_row_count,
            "duplicates_found": int(duplicate_count),
            "null_values": int(null_count),
            "is_healthy": int(duplicate_count) == 0 and int(null_count) == 0
        }
        
        return final_df, audit_report
