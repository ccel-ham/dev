import json
import socket
import time

import pyautogui as pygui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from GetDrivers import Connect, Setup

# https://www.instagram.com/coco3ndazo/
# https://www.instagram.com/coco3ndazo/live/


class InstaLiveRecorder:
    class BrowserSetup:
        def __init__(self) -> None:
            self.instagram_home_url = "https://www.instagram.com/"
            self.cookie_file_path = "cookies.json"
            self.driver = Setup().Chrome()
            self.load_cookies()

        def load_cookies(self):
            with open(self.cookie_file_path, "r") as file:
                cookies = json.load(file)
            self.driver.get(self.instagram_home_url)
            self.is_page_loaded_JS()

            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.get(self.instagram_home_url)
            self.is_page_loaded_JS()

        def is_page_loaded_JS(self):
            timeout = 5 * 60
            start_time = time.time()

            page_state = self.driver.execute_script("return document.readyState;")
            while time.time() - start_time < timeout:
                if page_state == "complete":
                    return True
                time.sleep(1)
                print("wait a second")
                page_state = self.driver.execute_script("return document.readyState;")
            print("time out")
            return False


def find_posision_by_image(path):
    location = pygui.locateOnScreen(path, confidence=0.8)
    if location:
        print(f"画像が見つかりました: {location}")
        return location
    else:
        print("画像が見つかりませんでした")
        return None


def click_center(location):
    center_point = pygui.center(location)
    pygui.click(center_point)


def main():
    record_browser = InstaLiveRecorder.BrowserSetup()

    record_browser.driver.get("https://www.instagram.com/anokorizumu/live/")
    body_element = record_browser.driver.find_element(By.TAG_NAME, "body")
    time.sleep(2)
    if body_element.text == "タップして再生":
        location = find_posision_by_image(r"./png/play.png")
        click_center(location)
        location = find_posision_by_image(r"./png/extensions.png")
        click_center(location)
        time.sleep(1)
        location = find_posision_by_image(r"./png/recorder.png")
        click_center(location)
        time.sleep(1)
        location = find_posision_by_image(r"./png/rec_start.png")
        click_center(location)
        time.sleep(1)
        print("Done")
    else:
        print("No")


main()
