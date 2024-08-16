import socket
import subprocess
import time
import threading

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from GetDrivers import Connect

class InstaLiveRecorder:
    class BrowserSetup():
        def __init__(self) -> None:
            self.instagram_home_url = "https://www.instagram.com/"
            self.browser_process = self.start_firefox()
            self.driver = self.connect_to_firefox()
            self.setup_complete = self.open_homepage()
            

        def start_firefox(self):
            # Firefoxを指定ポートで起動
            # exe command : firefox -marionette -start-debugger-server 2828 //only 2828
            firefox_process = subprocess.Popen(["firefox", "-marionette", "-start-debugger-server", "2828"])
            return firefox_process

        def connect_to_firefox(self):
            if self.wait_browser_lunched():
                driver = Connect().FireFox()
                return driver
            else:
                print("Browser lunch Error")

        def is_browser_running(self, host='localhost', port=2828):
            try:
                with socket.create_connection((host, port), timeout=2):
                    return True                
            except (ConnectionRefusedError, socket.timeout):
                return False

        def wait_browser_lunched(self, timeout=30, interval=2):
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self.is_browser_running():
                    return True
                print("wait a second")
                time.sleep(interval)
            return False
        
        def is_page_loaded_JS(self):
            timeout = 5*60
            start_time = time.time()

            page_state = self.driver.execute_script('return document.readyState;')
            while time.time() - start_time < timeout:
                if page_state == 'complete':
                    print("page has fully loaded.")
                    return True
                time.sleep(1)
                print("wait a second")
                page_state = self.driver.execute_script('return document.readyState;')
            print("time out")
            return False
        
        def open_homepage(self):
            self.driver.get(self.instagram_home_url)
            if self.is_page_loaded_JS():
                return True
            else:
                return False

def is_page_loaded_EC(driver):
    TIME_OUT = 60
    try:
        WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_all_elements_located
        )
        print("page has fully loaded.")
    except Exception as e:
        print("An error occurred: ", e)
    
def start_chrome(port=9222):
    # Chromeを指定ポートで起動
    command = [
        "chrome.exe",
        f"--remote-debugging-port={port}"
    ]
    subprocess.Popen(command)

def chrome_process():
    port=9222
    start_chrome(port)
    time.sleep(2)
    driver = Connect.Chrome(port)
    driver.get("https://www.instagram.com/")
    is_page_loaded_EC(driver)
    driver.minimize_window()

def main():
    record_browser = InstaLiveRecorder.BrowserSetup()
    if record_browser.open_homepage():
        print("Done")
    else:
        print("failure")

main()