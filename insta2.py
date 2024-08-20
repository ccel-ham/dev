import argparse
import json
import logging
import os
import random
import time
from datetime import datetime
from urllib.parse import urlparse

import pyautogui as pygui
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from yaspin import yaspin

from GetDrivers import Setup

# https://www.instagram.com/coco3ndazo/
# https://www.instagram.com/coco3ndazo/live/


class InstaLiveRecorder:
    class BaseConfig:
        def __init__(self, url):
            self.working_directry = r"C:\Users\ccelc\Desktop\python_folder\InstaLive"
            self.logger = logging.getLogger("InstaLive")
            self.logger_setup()
            self.url = url
            self.live_url = rf"{url}live/"

        def logger_setup(self):
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
                filename=rf"{self.working_directry}/insta.log",
                filemode="a",
            )

    class BrowserSetup:
        def __init__(self, config) -> None:
            self.logger = config.logger
            self.instagram_home_url = "https://www.instagram.com/"
            self.working_directry = config.working_directry
            self.target_home_url = config.url
            self.target_live_url = config.live_url
            self.cookie_file_path = rf"{config.working_directry}\cookies.json"
            self.extension_file_path = (
                rf"{config.working_directry}\InstaLive_Extensions\1.1.2_0.crx"
            )
            self.driver = Setup().Chrome(self.setup_options())
            self.driver.maximize_window()
            self.load_cookies()
            self.setup_afters()

        def setup_options(self):
            options = ChromeOptions()
            options.add_extension(f"{self.extension_file_path}")
            # options.add_argument(f"load-extension={self.extension_file_path}")
            prefs = {
                "download.default_directory": self.working_directry,
                "download.prompt_for_download": False,  # ダウンロード確認ダイアログを表示しない
                "download.directory_upgrade": True,  # フォルダをアップグレード
                "safebrowsing.enabled": True,  # セーフブラウジングを有効にする
            }
            options.add_experimental_option("prefs", prefs)
            return options

        def after_setup_tasks(self):
            # Extensionのタブを移動
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[1])
            time.sleep(0.5)
            # Instaの画面削除
            button = self.driver.find_element(By.XPATH, "//button[text()='後で']")
            button.click()

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
                page_state = self.driver.execute_script("return document.readyState;")
            self.logger.warning("Page Loading: Time Out")
            return False

        def wait_live_start(self, timeout_mimnutes=5):
            timeout = timeout_mimnutes * 60
            start_time = time.time()

            with yaspin(text="live start waiting ", color="yellow") as spinner:
                while time.time() - start_time < timeout:
                    if self.live_check():
                        spinner.write("Live Start")
                        self.logger.info("Live Start detected.")
                        return True
                    random_wait(min_seconds=5, max_seconds=15)
                self.logger.warning("Timeout: Live start")
                return False

        # ライブ • Instagram
        def live_check(self):
            self.open_page(self.target_live_url)
            time.sleep(2)
            if self.driver.title == "ライブ • Instagram":
                return True
            else:
                return False

        def open_page(self, url):
            self.driver.get(url)
            if self.is_page_loaded_JS():
                return True
            else:
                return False

    class RecordOperator:
        def __init__(self, config) -> None:
            self.working_directry = config.working_directry
            self.logger = config.logger
            self.target_home_url = config.url
            self.download_folder_name = self.get_download_folder_name()

        def find_posision_by_image(self, path, fixed_position):
            self.logger.info(f"Searching for image: {path}")
            location = pygui.locateOnScreen(path, confidence=0.8)
            if location:
                return location
            else:
                self.logger.warning("Image not found.")
                return fixed_position

        def click_center(self, location):
            center_point = pygui.center(location)
            self.logger.info(f"Clicking at center: {center_point}")
            pygui.click(center_point)
            random_wait(1, 2)

        def record_start(self):
            self.logger.info("Starting recording process.")
            # Point(x=953, y=571)
            location = self.find_posision_by_image(
                rf"{self.working_directry}/png/play.png", fixed_position=(953, 571)
            )
            self.click_center(location)
            # Point(x=1689, y=80)
            location = self.find_posision_by_image(
                rf"{self.working_directry}/png/extensions.png",
                fixed_position=(1689, 80),
            )
            self.click_center(location)
            # Point(x=1457, y=328)
            location = self.find_posision_by_image(
                rf"{self.working_directry}/png/recorder.png", fixed_position=(1457, 328)
            )
            self.click_center(location)
            # Point(x=1501, y=225)
            location = self.find_posision_by_image(
                rf"{self.working_directry}/png/rec_start.png",
                fixed_position=(1501, 225),
            )
            self.click_center(location)
            self.logger.info("Recording started.")

        def get_download_folder_name(self):
            username = self.extract_username()
            current_year = datetime.now().year
            download_folder_name = f"{username}_live_{current_year}"
            self.logger.info(f"Download folder name set to: {download_folder_name}")
            return download_folder_name

        def extract_username(self):
            parsed_url = urlparse(self.target_home_url)
            path = parsed_url.path
            username = path.strip("/").split("/")[0]
            return username

        def wait_live_end(self, timeout_hours=2, interval_minutes=5):
            timeout_seconds = timeout_hours * 3600  # タイムアウト時間を秒に変換
            interval_seconds = interval_minutes * 60  # インターバルを秒に変換
            start_time = time.time()
            cnt = 0
            with yaspin(text=f"Now Live On Air", color="yellow") as spinner:
                while True:
                    if os.path.isdir(
                        rf"{self.working_directry}\{self.download_folder_name}"
                    ):
                        spinner.write(f"Live Finish")
                        self.logger.info("Live finished.")
                        return True
                    elapsed_time = time.time() - start_time
                    if elapsed_time > timeout_seconds:
                        spinner.write(f"Live Time Out")
                        self.logger.warning("Timeout: Live End.")
                        return False
                    cnt += 1
                    spinner.text = f"Now Live On Air : counter {cnt}"
                    time.sleep(interval_seconds)


def random_wait(min_seconds=2, max_seconds=5):
    wait_time = random.uniform(min_seconds, max_seconds)
    time.sleep(wait_time)


def main(url):
    config = InstaLiveRecorder.BaseConfig(url=url)
    record_browser = InstaLiveRecorder.BrowserSetup(config)
    oparator = InstaLiveRecorder.RecordOperator(config)

    if not record_browser.open_page(record_browser.target_home_url):
        config.logger.warning("Login: Failure")
        return

    if not record_browser.wait_live_start():
        return

    body_element = record_browser.driver.find_element(By.TAG_NAME, "body")
    random_wait(1, 2)
    if body_element.text != "タップして再生":
        config.logger.warning("Live Page: Access Failure")
        return

    oparator.record_start()
    oparator.wait_live_end(interval_minutes=0.5)
    
    time.sleep(1 * 60)
    print("waiting systemclosed a minute")
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record Instagram live stream.")
    parser.add_argument(
        "--url", type=str, required=True, help="URL of the Instagram profile."
    )
    args = parser.parse_args()
    browser = main(args.url)
