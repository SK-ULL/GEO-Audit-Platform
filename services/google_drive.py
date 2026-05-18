import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = 'google-credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Replace with your actual Folder ID
FOLDER_ID = '1IwnrIdm6YpJw7k6k4kklbqIvIuU6tlDh'

def upload_to_drive(file_path):
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [FOLDER_ID]
        }
            
        media = MediaFileUpload(file_path, mimetype='application/pdf')
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"📁 PDF successfully archived to Google Drive. (ID: {file.get('id')})")
    except Exception as e:
        print(f"⚠️ Failed to upload to Drive: {e}")