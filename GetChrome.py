from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

class MyChrome:
    def __init__(self):
        self.chrome_driver_path = "/usr/bin/chromedriver"
        self.gecko_driver_path = "/usr/bin/geckodriver"

    def setup_Chrome(self):
        options = webdriver.ChromeOptions()
        service = ChromeService(executable_path=self.chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver
    
    def setup_FireFox(self):
        options = webdriver.FirefoxOptions()
        
        service = FirefoxService(executable_path=self.gecko_driver_path)
        driver = webdriver.Firefox(options=options, service=service)
        driver.implicitly_wait(10)
        return driver

if __name__ == "__main__":
    pass