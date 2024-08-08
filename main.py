import logging

from format  import DataFormatter
from api  import ApiManager
from drive import DriveManager


def main():
    id = "hitomi.yell.mana.g@gmail.com"
    passwd = "yell0000"
    api = ApiManager(id, passwd)
    if api.id_token is None:
        logging.error('Error: ID Token is None Login Failure')
        return
    api.get_data()
    update_data = DataFormatter().data_formatting(api.report)
    drive = DriveManager()
    drive.auth()
    if drive.drive in None:
        logging.error('Error: Drive is None GoogleDrive Auth Failure')
        return
    drive.update_file(update_data)
   

if __name__ == "__main__":
    main()


