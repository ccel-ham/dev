from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import json
import keyboard  # キーボード入力を監視するためのライブラリ
import time
import re  # 正規表現ライブラリ
import base64

import manga_downloader as md


def driver_setup():
    # Chromeのパフォーマンスログを有効にするためのオプション設定
    chrome_options = Options()
    user_data_dir = r"C:\Users\ccelc\Desktop\python_folder\selenium_profile"
    profile = r"bot"
    # chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    # chrome_options.add_argument(f"--profile-directory={profile}")
    chrome_options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL"}
    )  # パフォーマンスログを有効化

    # ChromeDriverのサービスを設定
    service = Service()

    # Chromeブラウザを起動
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

#comic = md.comic_site("mecha")
comic = md.comic_site("cmoa")
driver = driver_setup()
driver.get(comic.url)

print("監視を開始します。'q'キーを押すと終了します。")
try:
    while not keyboard.is_pressed("q"):
        logs = driver.get_log("performance")
        for entry in logs:
            if comic.is_target_url(entry):
                base64_data = md.get_blob_image(
                    driver,
                    comic.download_url,
                )
                comic.save(base64_data)
        time.sleep(0.25)
finally:
    comic.image_merge()
    with open("comic_urls.txt", "w") as file:
        for url in comic.matched_urls:
            file.write(url + "\n")
    print(f"{len(comic.matched_urls)} 件のURLが'matched_urls.txt'に保存されました。")
    print("ブラウザは開いたままです。手動で閉じてください。")
