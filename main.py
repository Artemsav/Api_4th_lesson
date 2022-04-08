import os
import time
import urllib
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from telegram import Bot


def fetch_spacex_last_launch(folder='images'):
    url = 'https://api.spacexdata.com/v4/launches/latest'
    flight_data = requests.get(url)
    flight_data_json = flight_data.json()
    images_urls = flight_data_json.get('links').get('flickr').get('original')
    path = Path().resolve()/folder
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


def fetch_nasa_apod(api_key, folder='images'):
    url = 'https://api.nasa.gov/planetary/apod'
    number_of_pictures = 10
    payload = {'api_key': api_key, 'count': number_of_pictures}
    path = Path().resolve()/folder
    Path(path).mkdir(parents=True, exist_ok=True)
    nasa_response = requests.get(url=url, params=payload)
    nasa_response_json = nasa_response.json()
    for index, image_inf in enumerate(nasa_response_json):
        image_url = image_inf.get('url')
        ext = get_extention(image_url)
        allowed_ext = ['.jpg', '.gif', '.png']
        if ext in allowed_ext:
            file_name = f'NASA{index}{ext}'
            named_path = f'{path}/{file_name}'
            response = requests.get(image_url)
            response.raise_for_status()
            with open(named_path, 'wb') as file:
                file.write(response.content)


def fetch_nasa_epic(api_key, folder='images'):
    payload = {'api_key': api_key}
    path = Path().resolve()/folder
    Path(path).mkdir(parents=True, exist_ok=True)
    url = 'https://api.nasa.gov/EPIC/api/natural/images?api_key=DEMO_KEY'
    nasa_response = requests.get(url)
    for index, _ in enumerate(nasa_response.json()):
        date, time = _.get('date').split()
        year, month, day = date.split('-')
        image_id = _.get('image')
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_id}.png'
        file_name = f'EPIC{index}.png'
        named_path = f'{path}/{file_name}'
        img_r = requests.get(url=image_url, params=payload)
        img_r.raise_for_status()
        with open(named_path, 'wb') as file:
            file.write(img_r.content)


def main():
    load_dotenv()
    api_key = os.getenv('NASA_API_KEY')
    token = os.getenv('TOKEN_TELEGRAM')
    user_id = os.getenv('CHANNEL_ID')
    sleep_time = os.getenv('SLEEP_TIME', 86400)
    fetch_spacex_last_launch()
    fetch_nasa_apod(api_key=api_key)
    fetch_nasa_epic(api_key=api_key)
    bot = Bot(token=token)
    while True:
        try:
            tree = os.walk('./images')
            for path, dirs, photos in tree:
                for photo in photos:
                    with open(f'./images/{photo}', 'rb') as file:
                        bot.send_photo(chat_id=user_id, photo=file)
                    os.remove(f'./images/{photo}')
                    time.sleep(10)
        except ConnectionError:
            time.sleep(60)
        except requests.exceptions.ReadTimeout:
            pass
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
