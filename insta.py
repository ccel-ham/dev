import socket
import subprocess
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from GetDrivers import Connect

PORT = 8080

def is_page_loaded_JS(driver):
    timeout = 5*60
    start_time = time.time()

    page_state = driver.execute_script('return document.readyState;')
    while time.time() - start_time < timeout:
        if page_state == 'complete':
            print("page has fully loaded.")
            return
        time.sleep(1)
        print("wait a second")
        page_state = driver.execute_script('return document.readyState;')

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

def start_firefox():
    # Firefoxを指定ポートで起動
    # exe command : firefox -marionette -start-debugger-server 2828 //only 2828
    subprocess.Popen(["firefox", "-marionette", "-start-debugger-server", "2828"])

def is_firefox_running(host='localhost'):
    port = 2828
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
        
    except (ConnectionRefusedError, socket.timeout):
        return False

def wait_for_firefox(timeout=30, interval=2):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_firefox_running():
            return True
        print("wait a second")
        time.sleep(interval)
    return False


def firefox_process():
    start_firefox()
    if wait_for_firefox():
        driver = Connect().FireFox()
        driver.get("https://www.instagram.com/")
        is_page_loaded_JS(driver)
        driver.minimize_window()


port=9222
start_chrome(port)
time.sleep(2)
driver = Connect.Chrome(port)
driver.get("https://www.instagram.com/")
is_page_loaded_EC(driver)
driver.minimize_window()

