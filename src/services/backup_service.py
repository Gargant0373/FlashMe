import os
import io
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
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

    folder_id = get_folder_id(service)

    # File metadata with parent folder ID
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    print(f"Uploaded file with ID: {file.get('id')}")
    
def get_folder_id(service, folder_name='FlashMe'):
    # Check if the folder already exists
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    folders = results.get('files', [])
    
    if folders:
        return folders[0]['id']
    else:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

def find_latest_backup_on_drive(service, folder_id):
    # List all files in the FlashMe folder
    query = f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name, modifiedTime)', orderBy='modifiedTime desc').execute()
    files = results.get('files', [])
    
    if not files:
        print("No backups found in Google Drive.")
        return None
    
    latest_file = files[0]
    print(f"Latest backup on Google Drive: {latest_file['name']} (ID: {latest_file['id']})")
    return latest_file

def download_file_from_drive(service, file_id, destination_path):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Download progress: {int(status.progress() * 100)}%")

def download_latest_backup_locally():
    creds = authenticate_user()
    if not creds:
        raise Exception("Authentication failed")

    service = build('drive', 'v3', credentials=creds)

    folder_id = get_folder_id(service, folder_name="FlashMe")

    # Find the latest backup file on Google Drive
    latest_backup = find_latest_backup_on_drive(service, folder_id)
    if latest_backup:
        file_id = latest_backup['id']
        file_name = 'flash_me.db'
        destination_path = file_name
        
        # Create backups folder if it doesn't exist
        if not os.path.exists("backups"):
            os.makedirs("backups")
        
        # Download the latest backup locally
        download_file_from_drive(service, file_id, destination_path)
        print(f"Latest backup downloaded to: {destination_path}")
    else:
        print("No backup found to download.")

def backup_and_upload():
    backup_path = backup_database()
    upload_to_google_drive(backup_path)    