import os
import time
import urllib
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from telegram import Bot


def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v4/launches/5eb87d42ffd86e000604b384'
    r = requests.get(url)
    api_r = r.json()
    images_urls = api_r.get('links').get('flickr').get('original')
    folder = 'images'
    home = Path().resolve()
    path = Path(home, folder)
    Path(path).mkdir(parents=True, exist_ok=True)
    for index, img_url in enumerate(images_urls):
        file_name = f'spacex{index}.jpg'
        named_path = f'{path}/{file_name}'
        responce = requests.get(img_url)
        responce.raise_for_status()
        with open(named_path, 'wb') as file:
            file.write(responce.content)


def get_extention(url):
    scheme, netloc, path, _, _, _ = urlparse(url)
    clean_path = urllib.parse.unquote(path)
    head, tail = os.path.split(clean_path)
    root, extention = os.path.splitext(tail)
    return extention


def fetch_nasa_apod():
    api_key = os.getenv('NASA_API_KEY')
    url = 'https://api.nasa.gov/planetary/apod'
    number_of_pictures = 50
    payload = {'api_key': api_key, 'count': number_of_pictures}
    r = requests.get(url=url, params=payload)
    api_r = r.json()
    for index, image_inf in enumerate(api_r):
        image_url = image_inf.get('url')
        folder = 'images'
        home = Path().resolve()
        path = Path(home, folder)
        Path(path).mkdir(parents=True, exist_ok=True)
        ext = get_extention(image_url)
        file_name = f'NASA{index}{ext}'
        named_path = f'{path}/{file_name}'
        responce = requests.get(image_url)
        responce.raise_for_status()
        with open(named_path, 'wb') as file:
            file.write(responce.content)


def fetch_nasa_epic():
    api_key = os.getenv('NASA_API_KEY')
    payload = {'api_key': api_key}
    url = 'https://api.nasa.gov/EPIC/api/natural/images?api_key=DEMO_KEY'
    r = requests.get(url)
    for index, _ in enumerate(r.json()):
        date, time = _.get('date').split()
        year, month, day = date.split('-')
        image_id = _.get('image')
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_id}.png'
        folder = 'images'
        home = Path().resolve()
        path = Path(home, folder)
        Path(path).mkdir(parents=True, exist_ok=True)
        ext = get_extention(url)
        file_name = f'EPIC{index}{ext}'
        named_path = f'{path}/{file_name}'
        img_r = requests.get(url=image_url, params=payload)
        img_r.raise_for_status()
        with open(named_path, 'wb') as file:
            file.write(img_r.content)


def main():
    token = os.getenv('TOKEN_TELEGRAM')
    user_id = os.getenv('USER_ID')
    bot = Bot(token=token)
    while True:
        try:
            tree = os.walk('./images')
            for address, dirs, photos in tree:
                for photo in photos:
                    bot.send_photo(chat_id=user_id, photo=open(f'./images/{photo}', 'rb'))
                    time.sleep(10)
        except ConnectionError:
            time.sleep(60)
        except requests.exceptions.ReadTimeout:
            pass
        break


if __name__ == '__main__':
    load_dotenv()
    #fetch_spacex_last_launch()
    #fetch_nasa_apod()
    #fetch_nasa_epic()
    main()
