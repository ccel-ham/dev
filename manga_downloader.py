from selenium.webdriver.common.by import By
import base64
import json
import re
import imghdr
from datetime import datetime
import os
from PIL import Image


BASE_DIRECTRY = r"C:\Users\ccelc\Desktop\test"

class comic_site:
    def __init__(self, site=None):
        self.site = site
        self.url=None
        self.re_blob=None
        self.download_url=None
        self.matched_urls = set()
        self.save_folder = create_folder()
        self.cnt = 1

        if site:
            self.url, self.re_blob = self.setup(site)
    
    def setup(self, site):
        site_map = {"mecha":{"url":"https://mechacomic.jp/",
                                  "re_blob":"blob:https://mechacomic.jp/"},
                    "cmoa":{"url":"https://www.cmoa.jp/", 
                            "re_blob":"blob:https://www.cmoa.jp/"}
                    }
        return site_map[site]["url"], site_map[site]["re_blob"]
    
    def is_target_url(self, entry):
        url = get_image_url(entry)
        if re.match(rf"^{self.re_blob}.+", url) is False:
            return False
        if url in self.matched_urls:
            return False
        self.download_url = url
        self.matched_urls.add(url)
        return True
    
    def save(self, base64_data):
        image_data = base64.b64decode(base64_data)
        ext = imghdr.what(None, image_data)
        path = self.make_save_path(ext)
        image_save(path, image_data)
        self.cnt += 1

    def make_save_path(self, ext):
        return os.path.join(self.save_folder, f"element_{str(self.cnt).zfill(4)}.{ext}")
    
    def image_merge(self):
        if self.site == "mecha":
            self.mecha_after_process()
        elif self.site == "cmoa":
            self.cmoa_after_process()


    def cmoa_after_process(self):
        """指定されたフォルダ内の画像を3つずつ順番に結合する関数"""
        image_files = [f for f in os.listdir(self.save_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        cnt = 0
        for i in range(0, len(image_files), 3):
            images_to_merge = image_files[i:i + 3]
            images = [Image.open(os.path.join(self.save_folder, img)) for img in images_to_merge]
            total_width = sum(image.width for image in images)
            max_height = max(image.height for image in images)
            merged_image = Image.new('RGB', (total_width, max_height))
            ext = imghdr.what(image_files[i])
            x_offset = 0
            for img in images:
                merged_image.paste(img, (x_offset, 0))
                x_offset += img.width
            output_filename = f"{str(cnt).zfill(4)}.{ext}"
            merged_image.save(os.path.join(self.save_folder, output_filename))

    def mecha_after_process(self):
        """指定されたフォルダ内のすべての画像を1つに結合する関数"""
        image_files = [f for f in os.listdir(self.save_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        images = [Image.open(os.path.join(self.save_folder, img)) for img in image_files]
        total_width = sum(image.width for image in images)
        max_height = max(image.height for image in images)

        merged_image = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for img in images:
            merged_image.paste(img, (x_offset, 0))
            x_offset += img.width
        ext = imghdr.what(image_files[0])
        output_filename = f"merged_image.{ext}"
        merged_image.save(os.path.join(self.save_folder, output_filename))

def create_folder(base_directory=BASE_DIRECTRY):
    today_date = datetime.now().strftime("%Y%m%d")
    folder_count = len(os.listdir(base_directory))
    new_folder_name = f"{today_date}_{str(folder_count).zfill(2)}"
    new_folder_path = os.path.join(base_directory, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    return new_folder_path

def get_image_ext(image_data):
    return imghdr.what(None, image_data)

def get_image_url(entry):
    log = json.loads(entry["message"])
    message = log["message"]
    if message["method"] != "Network.responseReceived":
        return ""

    response = message["params"]["response"]
    if response["mimeType"] != "image/png":
        return ""
    
    return response["url"]

def get_blob_image(driver, blob_url):
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

    driver.execute_script(script, blob_url)
    driver.implicitly_wait(5)
    base64_data = driver.find_element(By.TAG_NAME, "body").get_attribute("data-base64")

    if base64_data:
        return base64_data
    else:
        return None

def get_canvas_image(driver, canvas_element):
    image_data_url = driver.execute_script("return arguments[0].toDataURL('image/png');", canvas_element)
    base64_data = image_data_url.split(",")[1]
    if base64_data:
        return base64_data
    else:
        return None

def image_save(save_path, image_data):
    with open(save_path, "wb") as f:
            f.write(image_data)