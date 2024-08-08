from format  import DataFormatter
from api  import ApiManager
from drive import DriveManager


def main():
    id = "hitomi.yell.mana.g@gmail.com"
    passwd = "yell0000"
    api = ApiManager(id, passwd)
    if api.id_token is None:
        
        api.get_data()
    format = DataFormatter()
    update_data = format.data_formatting(api.report)

    a = 0

    

if __name__ == "__main__":
    main()


