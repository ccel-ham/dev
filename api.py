import requests
import json
from datetime import datetime, timedelta
import logging

class ApiManager:
    def __init__(self):
        self.login_url = 'https://api.portal.infomart.co.jp/api/v0.1/auth/signin'
        self.version_url = 'https://portal.infomart.co.jp/source_version'
        self.report_url = 'https://api.v-manage.restartz.co.jp/api/v0.1/routine/daily_reports'
        self.source_version = self.get_source_version()
        self.id_token = None

        

    def get_source_version(self):
        url = self.version_url
        headers = {
            'Accept-Language': 'ja-JP'
        }
        try:
            response = requests.get(url, headers=headers, proxies=self.proxies)
            response.raise_for_status()
            return int(response.text)
        except requests.RequestException as e:
            logging.error('Error: %s', e)
            return None

    def login(self):
        url = self.login_url
        payload = {
            "userid": "hitomi.yell.mana.g@gmail.com",
            "passwd": "yell0000",
            "front_version": self.source_version
        }
        headers = {
            'Accept-Language': 'ja-JP',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            info = response.json()
            self.id_token = info["result"]["AuthenticationResult"]["IdToken"]
            logging.info(response.text)
        except requests.RequestException as e:
            logging.error('Error: %s', e)

    def get_last_day_and_days_of_previous_month(self):
        now = datetime.now()
        current_month = now.month
        current_year = now.year

        if current_month == 1:
            last_day_of_previous_month = datetime(current_year - 1, 12, 31)
        else:
            last_day_of_previous_month = datetime(current_year, current_month, 1) - timedelta(days=1)

        last_date = last_day_of_previous_month.day
        days_in_previous_month = last_date

        return {
            'lastDate': last_day_of_previous_month.strftime("%Y-%m-%d"),
            'daysInPreviousMonth': days_in_previous_month
        }

    def get_data(self):
        dates_info = self.get_last_day_and_days_of_previous_month()
        last_date = dates_info['lastDate']
        days_in_previous_month = dates_info['daysInPreviousMonth']
        url = self.report_url
        payload = {
            "staff_id": "d7e04f0b-b934-48da-a8e8-db281c8eacbd",
            "shop_id": "1bcd9cfb-fb4d-44dc-be95-ee247ebe66b7",
            "spec_date": last_date,
            "request_day_count": days_in_previous_month,
            "withlogs": 0,
            "id_token": self.id_token,
            "front_version": self.source_version
        }
        headers = {
            'Accept-Language': 'ja-JP',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            info = response.json()
            self.id_token = info["result"]["AuthenticationResult"]["IdToken"]
            logging.info(response.text)
        except requests.RequestException as e:
            logging.error('Error: %s', e)

# 使用例
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    api_manager = ApiManager()
    api_manager.login()
    api_manager.get_data()
