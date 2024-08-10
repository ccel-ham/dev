import logging
from spin import spinner
from spin import SpinText
import time

from format  import DataFormatter
from api  import ApiManager



def main():
    id = "hitomi.yell.mana.g@gmail.com"
    passwd = "yell0000"
    api = ApiManager(id, passwd)
    if api.id_token is None:
        logging.error('Error: ID Token is None Login Failure')
        return
    api.get_data()
    update_data = DataFormatter().data_formatting(api.report)
   
@spinner(SpinText.scraping)
def main1():
    time.sleep(2)
    return False



if __name__ == "__main__":
    main()
