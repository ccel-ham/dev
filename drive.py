from pathlib import Path
import mimetypes

from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class DriveManager:
    def __init__(self) -> None:
        self.UPLOAD_FOLDER_ID = "13F4XqYgR9GGbH8mBAU05nzyVnze9WhB2"
        self.working_directry = Path.cwd()
        self.credentials_path = self.working_directry.joinpath("credentials.json")
        print(self.credentials_path)
        self.drive = None
    
    def auth(self):
        gauth = GoogleAuth()
        scope = ["https://www.googleapis.com/auth/drive"]

        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_path, scope
        )
        self.drive = GoogleDrive(gauth)
        print("Google Drive Authentication Success")

    
    def get_file_info(self, file_path):
        path = Path(file_path)
        file_name = path.name
        mime_type, _ = mimetypes.guess_type(file_path)
        
        return file_name, mime_type

    def upload_file(self, local_file_path):
        
        file_name , mime_type = self.get_file_info(local_file_path)
        file_metadata = {
            'title': file_name,
            'mimeType': mime_type,
            'parents': [{'id': self.UPLOAD_FOLDER_ID}]
        }

        
        file = self.drive.CreateFile(file_metadata)
        file.SetContentFile(local_file_path)
        file.Upload()
        print(f'File uploaded: https://drive.google.com/file/d/{file["id"]}')


local_file_path = "/workspaces/card_pdf/vba_cover.mp4"
 
drive = DriveManager()
drive.auth()
drive.upload_file(local_file_path)