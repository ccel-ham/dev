from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import json
import keyboard  # キーボード入力を監視するためのライブラリ
import time
import re  # 正規表現ライブラリ
import base64
import imghdr

import manga_downloader as md

def driver_setup():
    # Chromeのパフォーマンスログを有効にするためのオプション設定
    chrome_options = Options()
    user_data_dir = r"C:\Users\ccelc\Desktop\python_folder\selenium_profile"
    profile = r"bot"
    # chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    # chrome_options.add_argument(f"--profile-directory={profile}")

    # ChromeDriverのサービスを設定
    service = Service()
    # Chromeブラウザを起動
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# 任意のURLにアクセス
driver = driver_setup()
driver.get("https://renta.papy.co.jp/")

print("監視を開始します。'q'キーを押すと終了します。")

# マッチしたURLを保存するリスト
matched_urls = set()
cnt = 0
try:
    while not keyboard.is_pressed("q"):
        matching_elements = []
        # "pageWrap"クラス名を持つすべてのdiv要素を取得
        page_wrap_elements = driver.find_elements(By.CLASS_NAME, "pageWrap")

        # 各pageWrap要素を確認
        for page_wrap in page_wrap_elements:
            div_elements = page_wrap.find_elements(By.TAG_NAME, 'div')
            # 子要素の中で、data-writed属性が"1"の要素を探す
            for child_div in div_elements:
                if child_div.get_attribute('data-writed') == '1':
                    data_num = child_div.get_attribute('data-num')
                    if data_num not in matched_urls:
                        matched_urls.add(data_num)
                        canvas_element = page_wrap.find_element(By.TAG_NAME, 'canvas')
                        base64_data = md.get_canvas_image(driver, canvas_element)
                        image_data = base64.b64decode(base64_data)
                        # 画像形式を自動判定
                        ext = imghdr.what(None, image_data)
                        if ext is None:
                            print("画像形式を判定できませんでした。デフォルトでpngとして保存します。")
                            ext = "png"  # デフォルトの拡張子を設定

                        file_name = f"canvas_image.{ext}"
                        with open(file_name, "wb") as file:
                            file.write(image_data)


    
    
    time.sleep(0.25)
finally:
    with open("matched_urls.txt", "w") as file:
        for url in matched_urls:
            file.write(url + "\n")
    print(f"{len(matched_urls)} 件のURLが'matched_urls.txt'に保存されました。")
    print("ブラウザは開いたままです。手動で閉じてください。")
