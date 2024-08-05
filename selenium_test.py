#https://tokensniffer.com/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json

result_data = {}

def wait_element_appearance(driver):
    TIME_OUT = 20
    WebDriverWait(driver, TIME_OUT).until(
        EC.presence_of_all_elements_located
    )

def save_text_file():
    file_name = "result_data.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(result_data, file, ensure_ascii=False, indent=4)



def extract_locate(text):
    pattern = r'【(.*?)】'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

def extract_date(text):
    pattern = r'\d{2}月\d{2}日（[日月火水木金土]）'
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None

def extract_date_locate(driver):
    worked_cards = driver.find_elements(By.CLASS_NAME, "card-head")
    for card in worked_cards:
        text = card.text
        date = extract_date(text)
        locate = extract_locate(text)
        print(f"{date}  -- {locate}")
        if date in result_data:
            result_data[date].append(locate)
        else:
            result_data[date] = [locate]
         

def if_element():
    password = "yell0000"
    id = "hitomi.yell.mana.g@gmail.com"
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get("https://portal.infomart.co.jp/api/v0.1/auth/signin")

    wait_element_appearance(driver)

    id_input = driver.find_element(By.ID, 'input_email')
    id_input.send_keys(id)
    time.sleep(1)
    pass_input = driver.find_element(By.ID, 'input_password')
    pass_input.send_keys(password)
    time.sleep(1)
    enter_button = driver.find_elements(By.CLASS_NAME, "step-primary")
    enter_button[0].click()
    
    wait_element_appearance(driver)
    services = driver.find_elements(By.CLASS_NAME, "home-service-name")
    for service in services:
        if service.text == "V-Manage":
            service.click()
            break
    
    wait_element_appearance(driver)
    v_side_bars = driver.find_elements(By.CLASS_NAME, "v-btn__content")
    for v_side_bar in v_side_bars:
        if v_side_bar.text == "日報・引継ぎ":
            v_side_bar.click()
            time.sleep(5)
            break

    for cnt in range(1,5):
        wait_element_appearance(driver)
        v_side_bars = driver.find_elements(By.CLASS_NAME, "v-btn__content")
        for v_side_bar in v_side_bars:
            if v_side_bar.text == "前の7日間":
                extract_date_locate(driver)
                v_side_bar.click()
                print(f"{cnt} th ")
                time.sleep(5)

    print(result_data)
if __name__ == '__main__':
    if_element()
    save_text_file()