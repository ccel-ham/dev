from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

class DriverPath:
    chrome_driver_path= "/usr/bin/chromedriver"
    gecko_driver_path = "/usr/bin/geckodriver"

class Setup:
    def __init__(self):
        pass

    def Chrome(self):
        options = webdriver.ChromeOptions()
        service = ChromeService(executable_path=DriverPath.chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver
    
    def FireFox(self):
        options = webdriver.FirefoxOptions()
        
        service = FirefoxService(executable_path=DriverPath.gecko_driver_path)
        driver = webdriver.Firefox(options=options, service=service)
        driver.implicitly_wait(10)
        return driver


class Connect:
    def __init__(self):
        pass

    def Chrome(self, port):
        service = ChromeService(executable_path=DriverPath.chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver

    
    def FireFox(self):
        debugg_port = "2828"
        options = webdriver.FirefoxOptions()
        options.set_preference("devtools.debugger.remote-enabled", True)
        options.set_preference("devtools.debugger.remote-port", debugg_port)
        
        # FirefoxDriverのサービスを作成
        service = FirefoxService(executable_path=DriverPath.gecko_driver_path, service_args=['--marionette-port', debugg_port, '--connect-existing'])

        # FirefoxDriverを指定ポートで起動したFirefoxブラウザに接続
        driver = webdriver.Firefox(service=service, options=options)
        return driver


if __name__ == "__main__":
    pass