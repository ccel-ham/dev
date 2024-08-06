pip install selenium selenium-wire

from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Firefoxドライバーを設定
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# ページにアクセス
driver.get("https://example.com")

# ページ読み込みを待機
driver.implicitly_wait(10)

# ネットワークリクエストをキャプチャ
for request in driver.requests:
    if request.response:
        if 'XMLHttpRequest' in request.headers.get('X-Requested-With', ''):
            print(f"URL: {request.url}")
            print(f"Method: {request.method}")
            print(f"Headers: {request.headers}")
            print(f"Response Status Code: {request.response.status_code}")
            print("\n")

# ブラウザを閉じる
driver.quit()
