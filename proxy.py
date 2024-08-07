import requests
import main

url = "https://www.keihan.co.jp/"
headers = {
    'Accept-Language': 'ja-JP'
}
proxies = {
    'http': 'http://20.210.113.32',
}

response = requests.get(url, headers=headers, proxies=proxies)
response.encoding = 'utf-8'
response.raise_for_status()
main.save_text_file(response.text, "proxy.txt")
if "遅れ" in response.text:
    print(f"True {proxies}")