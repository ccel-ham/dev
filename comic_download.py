from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import keyboard  # キーボード入力を監視するためのライブラリ
import time
import re  # 正規表現ライブラリ
import base64


def download_blob_image(driver, blob_url, save_path):
    # JavaScriptを使ってblobデータを取得するスクリプト
    script = """
    var xhr = new XMLHttpRequest();
    xhr.open('GET', arguments[0], true);
    xhr.responseType = 'blob';
    xhr.onload = function() {
        var reader = new FileReader();
        reader.onloadend = function() {
            // base64エンコードされたデータを返す
            var base64data = reader.result.split(',')[1];
            document.body.setAttribute('data-base64', base64data);
        };
        reader.readAsDataURL(xhr.response);
    };
    xhr.send();
    """

    # JavaScriptを実行してblobデータを取得
    driver.execute_script(script, blob_url)

    # 少し待機してデータを読み取る
    driver.implicitly_wait(5)

    # base64エンコードされたデータを取得
    base64_data = driver.find_element(By.TAG_NAME, "body").get_attribute("data-base64")

    if base64_data:
        # base64データをデコードしてファイルに保存
        with open(save_path, "wb") as f:
            f.write(base64.b64decode(base64_data))
        print(f"画像が保存されました: {save_path}")
    else:
        print("画像の取得に失敗しました。")


cnt = 0
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

# 任意のURLにアクセス
driver.get("https://mechacomic.jp")

print("監視を開始します。'q'キーを押すと終了します。")

# マッチしたURLを保存するリスト
matched_urls = set()

try:
    while not keyboard.is_pressed("q"):
        # パフォーマンスログの取得
        logs = driver.get_log("performance")

        # ログをフィルタリングして表示
        for entry in logs:
            log = json.loads(entry["message"])  # ログエントリをJSON形式でパース
            message = log["message"]

            # レスポンスが受信されたときのイベントをキャプチャ
            if message["method"] == "Network.responseReceived":
                response = message["params"]["response"]
                request_id = message["params"]["requestId"]

                # GETリクエストであり、content-typeがimage/pngの場合のみ表示
                if response["mimeType"] == "image/png":
                    url = response["url"]

                    # 正規表現にマッチするURLを保存
                    if re.match(r"^blob:https://mechacomic.jp/.+", url):
                        if url not in matched_urls:
                            download_blob_image(
                                driver,
                                url,
                                rf"C:\Users\ccelc\Desktop\test\aoshimakun_{str(cnt).zfill(3)}.webp",
                            )
                            cnt += 1
                            matched_urls.add(url)

        # CPU負荷を軽減するため少し待機
        time.sleep(0.5)
finally:
    # 監視終了後にURLをファイルに保存
    with open("matched_urls.txt", "w") as file:
        for url in matched_urls:
            file.write(url + "\n")
    print(f"{len(matched_urls)} 件のURLが'matched_urls.txt'に保存されました。")
    print("ブラウザは開いたままです。手動で閉じてください。")
