from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json
import random

from GetChrome import MyChrome


class FportalLogin():
    def __init__(self):
        self.login_url = "https://portal.infomart.co.jp/api/v0.1/auth/signin"
        self.result_data = {}
        self.driver = MyChrome().setup_Chrome()

    def wait_element_appearance(self):
        TIME_OUT = 60
        WebDriverWait(self.driver, TIME_OUT).until(
            EC.presence_of_all_elements_located
        )
    
    def random_sleep(self):
        time.sleep(self.generate_random_float())

    def generate_random_float(self):
        MIN = 3
        MAX = 5
        return round(random.uniform(MIN, MAX), 2)

    def save_text_file(self):
        file_name = "result_data.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.result_data, file, ensure_ascii=False, indent=4)
        return file_name


    def extract_locate(seelf, text):
        pattern = r'【(.*?)】'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None

    def extract_date(self, text):
        pattern = r'\d{2}月\d{2}日（[日月火水木金土]）'
        match = re.search(pattern, text)
        if match:
            return match.group()
        else:
            return None

    def extract_date_locate(self):
        worked_cards = self.driver.find_elements(By.CLASS_NAME, "card-head")
        for card in worked_cards:
            text = card.text
            date = self.extract_date(text)
            locate = self.extract_locate(text)
            print(f"{date}  -- {locate}")
            if date in self.result_data:
                self.result_data[date].append(locate)
            else:
                self.result_data[date] = [locate]
        
    
    def login(self, id, password):
        self.driver.get(self.login_url)
        self.wait_element_appearance()
        
        id_input = self.driver.find_element(By.ID, 'input_email')
        id_input.send_keys(id)
        self.random_sleep()
        
        pass_input = self.driver.find_element(By.ID, 'input_password')
        pass_input.send_keys(password)
        self.random_sleep()
        
        enter_button = self.driver.find_elements(By.CLASS_NAME, "step-primary")
        enter_button[0].click()

    def login_complete_check(self):
        self.wait_element_appearance(self.driver)
        LOGIN_TOPPAGE_TITLE = "F-Portal | ホーム"
        if self.driver.title == LOGIN_TOPPAGE_TITLE:
            print("Log-In Complete")
            return True
        else:
            print("Log-In Failure")
            return False        
        
    def find_element_by_classname_text(self, class_name, text):
        self.wait_element_appearance(self.driver)
        self.random_sleep()
        elements = self.driver.find_elements(By.CLASS_NAME, class_name)
        for element in elements:
            if element.text == text:
                return element
        return None

    def data_extract_process(self):
        for cnt in range(1, 5):
            self.wait_element_appearance(self.driver)
            self.random_sleep()
            element = self.find_element_by_classname_text(class_name="v-btn__content", text="前の7日間")
            self.extract_date_locate(self.driver)
            element.click()
            print(f"{cnt} th ")
            time.sleep(5)
        print(self.result_data)

if __name__ == '__main__':
    #pass
    password = "yell0000"
    id = "hitomi.yell.mana.g@gmail.com"
    portal = FportalLogin()
    portal.login(id, password)
    if portal.login_complete_check():
        element = portal.find_element_by_classname_text(class_name="home-service-name", text="V-Manage")
        element.click()
        
        element = portal.find_element_by_classname_text(class_name="home-service-name", text="日報・引継ぎ")
        element.click()

        portal.data_extract_process()
        print("data extract is done ")
        
        




