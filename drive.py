from pathlib import Path

from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class DriveManager:
    def __init__(self) -> None:
        self.que_url = "https://script.google.com/macros/s/AKfycbzngUnlWu7eEt-iCQAGoAIsArQBEkMvF_Ogmv9PNz55qTd1G44ER0yNVV0HkIG-Bx3haA/exec"
        self.target_file_id = "1KqSGpCFVRpv-QaYn2uYIG7vU_UUe7MJj"
        self.credentials_path = self.get_credential_path()
        self.drive = None
    

    def get_credential_path(self):
        current_directory = Path(__file__).parent
        parent_directory = current_directory.parent
        credentials_path = parent_directory.joinpath("credentials.json")
        return credentials_path
    
    def auth(self):
        gauth = GoogleAuth()
        scope = ["https://www.googleapis.com/auth/drive"]

        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            str(self.credentials_path), scope
        )
        self.drive = GoogleDrive(gauth)
        print("Google Drive Authentication Success")

    
    def update_file(self, report_data):
        file = self.drive.CreateFile({'id':self.target_file_id})
        file.SetContentString(report_data)
        file.Upload()
        print(f'File updated: Success')

    def que_post(self):
        pass


if __name__ == '__main__':
    pass