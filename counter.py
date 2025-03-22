import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os


def shorten_link(token, url, link):
    method_name = "utils.getShortLink"
    payload = {"access_token": token, "v": "5.199", "url": link}
    response = requests.get(url + method_name, params=payload)
    response.raise_for_status()
    return response.json()['response']["short_url"]


def count_clicks(token, url, ready_url):
    method_name = "utils.getLinkStats"
    parsed = urlparse(ready_url)
    key = parsed.path[1:]
    payload = {"access_token": token, "key": key, "interval": "forever", "v": "5.199"}
    response = requests.get(url + method_name, params=payload)
    response.raise_for_status()
    clicks_count = response.json()['response']["stats"][0]["views"]
    return clicks_count


def is_shorten_link(url):
    return True if urlparse(url).netloc == "vk.cc" else False


if __name__ == "__main__":
    load_dotenv()
    url = "https://api.vk.ru/method/"
    token = os.environ['TOKEN']
    try:
        link = input("Введите ссылку: ")
        if is_shorten_link(link):
            click_num = count_clicks(token, url, link)
            print(f"Просмотрела: {click_num} человека")
        else:
            shorted_link = shorten_link(token, url, link)
            print(f"Сокращенная ссылка: {shorted_link}")
    except requests.exceptions.HTTPError:
        print("Возникла ошибка при попытке обращения к серверу.")