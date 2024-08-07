import requests

#激遅 161.34.40.109:3128
set_proxy = "185.243.218.202"

check_ip_url = "https://api.ipify.org/"
headers = {
    'Accept-Language': 'ja-JP'
}
proxies = {
    'http': f'http://{set_proxy}',
    'https': f'http://{set_proxy}',
}

response = requests.get(check_ip_url, headers=headers, proxies=proxies)
response.encoding = 'utf-8'
response.raise_for_status()
print(response.text)