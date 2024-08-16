import time

import requests

from api import ApiManager
from spin import SpinText, spinner


@spinner(SpinText.post)
def data_post_to_spread_heet(data):
    GOOGLE_URL = "https://script.google.com/macros/s/AKfycbzngUnlWu7eEt-iCQAGoAIsArQBEkMvF_Ogmv9PNz55qTd1G44ER0yNVV0HkIG-Bx3haA/exec"
    payload = {
        "pass":"9999",
        "report_data":data
    }
    headers = {
        'Accept-Language': 'ja-JP',
        'Content-Type': 'application/json'
    }
    response = requests.post(GOOGLE_URL
    , headers=headers, json=payload)
    response.raise_for_status()
    info = response.json()
    print(info["message"])
    return True

def main():
    scraping_start_time = time.time()
    password = "yell0000"
    id = "hitomi.yell.mana.g@gmail.com"
    print("Scraping Start -- >>", end="")
    api_manager = ApiManager(id=id, passwd=password)
    api_manager.login()
    api_manager.get_report()
    scraping_end_time = time.time()
    print(f' {(scraping_end_time - scraping_start_time):.2f} sec')

    posting_start_time = time.time()
    print("Data Posting Start -- >>", end="")
    data_post_to_spread_heet(api_manager.report)
    posting_end_time = time.time()
    print(f'time -- {(posting_end_time - posting_start_time):.2f} sec')


if __name__ == "__main__":
    main()