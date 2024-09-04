import os
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from services.auth_service import authenticate_user

def backup_database(db_path = "flash_me.db", backup_dir="backups"):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    backup_filename = f"flash_me_backup.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    shutil.copy2(db_path, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path

def upload_to_google_drive(file_path):
    creds = authenticate_user()
    if not creds:
        raise Exception("Authentication failed")
    
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded file with ID: {file.get('id')}")
    
def backup_and_upload():
    backup_path = backup_database()
    upload_to_google_drive(backup_path)    