from pathlib import Path
import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse
import urllib


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

if __name__ == '__main__':
    load_dotenv()
    #fetch_spacex_last_launch()
    fetch_nasa_apod()
