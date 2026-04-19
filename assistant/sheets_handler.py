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
        self.service = build('sheets', 'v4', credentials=self.creds)

    def _load_credentials(self):
        # 1. Try loading from Base64 (Production/Vercel strategy)
        if self.service_account_json:
            try:
                decoded_json = base64.b64decode(self.service_account_json).decode('utf-8')
                creds_info = json.loads(decoded_json)
                return service_account.Credentials.from_service_account_info(creds_info, scopes=self.scopes)
            except Exception as e:
                print(f"CRITICAL: Failed to parse GOOGLE_SERVICE_ACCOUNT_JSON. Detail: {e}")

        # 2. Try loading from local file (Local dev strategy)
        if self.credentials_path and os.path.exists(self.credentials_path):
            return service_account.Credentials.from_service_account_file(self.credentials_path, scopes=self.scopes)
        
        raise ValueError("No Google credentials found (Check GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_CREDENTIALS_PATH)")

    def get_sheet_data(self, spreadsheet_id):
        try:
            # Dynamically get the first sheet name to be resilient to tab renaming
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

            # Convert to DataFrame for robust analysis
            df = pd.DataFrame(values[1:], columns=values[0])
            
            # Step 1: Perform Audit
            cleaned_df, audit_report = self.validate_data(df)
            
            return cleaned_df.to_string(index=False), audit_report
        except Exception as e:
            return f"Error accessing Sheets: {str(e)}", {}

    def validate_data(self, df):
        """
        Performs a data integrity audit on the provided dataframe.
        """
        initial_row_count = len(df)
        
        # 1. Detect Duplicates
        duplicate_count = df.duplicated().sum()
        df_no_dupes = df.drop_duplicates()
        
        # 2. Detect Nulls
        null_count = df_no_dupes.isnull().sum().sum() + (df_no_dupes == "").sum().sum()
        # Fill nulls with 'N/A' so the AI doesn't hallucinate missing values
        final_df = df_no_dupes.replace("", "N/A").fillna("N/A")
        
        audit_report = {
            "rows_checked": initial_row_count,
            "duplicates_found": int(duplicate_count),
            "null_values": int(null_count),
            "is_healthy": duplicate_count == 0 and null_count == 0
        }
        
        return final_df, audit_report
