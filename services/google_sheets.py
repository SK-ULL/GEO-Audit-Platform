import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

SERVICE_ACCOUNT_FILE = 'google-credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Replace with your actual Sheet ID
SPREADSHEET_ID = '1BcQQl_ucHK38Yd-j03jx5rLOo7I3Q4YpNHMRq_uQujs' 

def log_lead_to_sheets(name, email, company, status):
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        
        range_name = 'Sheet1!A:E' # Assumes your first tab is named Sheet1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        values = [[name, email, company, timestamp, status]]
        body = {'values': values}
        
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, 
            range=range_name,
            valueInputOption='USER_ENTERED', 
            body=body
        ).execute()
        print(f"📊 Lead successfully logged to Google Sheets.")
    except Exception as e:
        print(f"⚠️ Failed to log to Sheets: {e}")