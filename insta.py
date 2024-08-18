import argparse
import os
import random
import socket
import subprocess
import sys
import time
from datetime import datetime
from urllib.parse import urlparse

from yaspin import yaspin
import pyautogui as pygui
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from GetDrivers import Connect

# https://www.instagram.com/coco3ndazo/
# https://www.instagram.com/coco3ndazo/live/


class InstaLiveRecorder:
    directry = r"C:\Users\ccelc\Desktop\python_folder\InstaLive"

    class BrowserSetup:
        def __init__(self, port) -> None:
            self.instagram_home_url = "https://www.instagram.com/"
            self.port = port
            self.browser_process = self.start_chrome(port)
            self.driver = self.connect_to_chrome(port)

        def start_chrome(self, port):
            # Chromeを指定ポートで起動
            command = [
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                f"--remote-debugging-port={port}",
            ]
            chrome_process = subprocess.Popen(command)
            return chrome_process

        def connect_to_chrome(self, port):
            if self.wait_browser_lunched(port):
                time.sleep(2)
                driver = Connect().Chrome(port)
                print("browser connect success")
                driver.maximize_window()
                return driver
            else:
                print("Browser lunch Error")
                return False

        def is_browser_running(self, host="localhost", port=2828):
            try:
                with socket.create_connection((host, str(port)), timeout=2):
                    return True
            except (ConnectionRefusedError, socket.timeout):
                return False

        def wait_browser_lunched(self, port, timeout=30, interval=2):
            start_time = time.time()
            print(f"check to browser running")
            while time.time() - start_time < timeout:
                if self.is_browser_running(port=port):
                    return True
                print("wait a second")
                time.sleep(interval)
            return False

        def is_page_loaded_JS(self):
            timeout = 5 * 60
            start_time = time.time()
            print("page loading now")
            page_state = self.driver.execute_script("return document.readyState;")
            while time.time() - start_time < timeout:
                if page_state == "complete":
                    return True
                time.sleep(1)
                print("wait a second")
                page_state = self.driver.execute_script("return document.readyState;")
            print("time out")
            return False

        def open_page(self, url):
            self.driver.get(url)
            if self.is_page_loaded_JS():
                return True
            else:
                return False

    class RecordOperator:
        def __init__(self, url) -> None:
            self.target_home_url = url
            self.target_live_url = f"{url}live/"
            self.download_folder_name = self.get_download_folder_name()

        def wait_live_start(self, timeout_mimnutes=5):
            timeout = timeout_mimnutes * 60
            start_time = time.time()

            with yaspin(text="live start waiting ", color="yellow") as spinner:
                while time.time() - start_time < timeout:
                    if self.live_check():
                        spinner.write("Live Start")
                        return True
                    self.random_wait(min_seconds=20, max_seconds=60)
                return False

        def live_check(self):
            res = requests.get(self.target_live_url)
            if res.status_code == 200:
                return True
            else:
                return False

        def find_posision_by_image(self, path):
            location = pygui.locateOnScreen(path, confidence=0.8)
            if location:
                print(f"画像が見つかりました: {location}")
                return location
            else:
                print("画像が見つかりませんでした")
                return None

        def click_center(self, location):
            center_point = pygui.center(location)
            print(center_point)
            pygui.click(center_point)
            self.random_wait(1, 2)

        def record_start(self):
            # Point(x=953, y=571)
            location = self.find_posision_by_image(
                rf"{InstaLiveRecorder.directry}/png/play.png"
            )
            self.click_center(location)
            # Point(x=1689, y=80)
            location = self.find_posision_by_image(
                rf"{InstaLiveRecorder.directry}/png/extensions.png"
            )
            self.click_center(location)
            # Point(x=1457, y=328)
            location = self.find_posision_by_image(
                rf"{InstaLiveRecorder.directry}/png/recorder.png"
            )
            self.click_center(location)
            # Point(x=1501, y=225)
            location = self.find_posision_by_image(
                rf"{InstaLiveRecorder.directry}/png/rec_start.png"
            )
            self.click_center(location)
            print("Rec Start")

        def random_wait(self, min_seconds=2, max_seconds=5):
            wait_time = random.uniform(min_seconds, max_seconds)
            time.sleep(wait_time)

        def get_download_folder_name(self):
            username = self.extract_username()
            current_year = datetime.now().year
            self.download_folder_name = f"{username}_live_{current_year}"
            print(self.download_folder_name)

        def extract_username(self):
            parsed_url = urlparse(self.target_home_url)
            path = parsed_url.path
            username = path.strip("/").split("/")[0]
            return username

        def wait_live_end(self, timeout_hours=2, interval_minutes=5):
            timeout_seconds = timeout_hours * 3600  # タイムアウト時間を秒に変換
            interval_seconds = interval_minutes * 60  # インターバルを秒に変換
            start_time = time.time()

            with yaspin(text="Now Live On Air ", color="yellow") as spinner:
                while True:
                    if os.path.isdir(
                        rf"C:\Users\ccelc\Downloads\{self.download_folder_name}"
                    ):
                        spinner.write(f"Live Finish")
                        return True
                    elapsed_time = time.time() - start_time
                    if elapsed_time > timeout_seconds:
                        spinner.write(f"Live Time Out")
                        return False

                    time.sleep(interval_seconds)


def log_arguments_to_file():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    script_name = os.path.basename(__file__)
    arguments = " ".join(sys.argv[1:])
    log_content = (
        f"Time: {current_time}\nScript: {script_name}\nArguments: {arguments}\n\n"
    )
    with open(rf"{InstaLiveRecorder.directry}\log.txt", "a") as log_file:
        log_file.write(log_content)
    print("Arguments have been logged.")


def main(url, port=9222):
    log_arguments_to_file()
    record_browser = InstaLiveRecorder.BrowserSetup(port)
    oparator = InstaLiveRecorder.RecordOperator(url)
    if not record_browser.open_page(oparator.target_home_url):
        print("failure")
        return

    if not oparator.wait_live_start():
        print("TIME OUT : live not start")
        return

    record_browser.open_page(oparator.target_live_url)
    body_element = record_browser.driver.find_element(By.TAG_NAME, "body")
    oparator.random_wait()
    if body_element.text != "タップして再生":
        print("Live page access Failure")
        return

    oparator.record_start()
    oparator.wait_live_end()

    return


# https://www.instagram.com/coco3ndazo/

# cmd python C:\Users\ccelc\Desktop\python_folder\InstaLive\insta.py --url "https://www.instagram.com/shota_watanabe_sn_official/" --port 9222

main(url="https://www.instagram.com/koromami24/", port=9222)

if __name__ != "__main__":
    parser = argparse.ArgumentParser(description="Record Instagram live stream.")
    parser.add_argument(
        "--url", type=str, required=True, help="URL of the Instagram profile."
    )
    parser.add_argument(
        "--port", type=int, required=False, help="Port number for the browser instance."
    )

    args = parser.parse_args()
    browser = main(args.url, args.port)
