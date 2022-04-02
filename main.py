from urllib import response
import requests
from pathlib import Path
from urllib.parse import urlsplit

def download_image(url, folder):
    home = Path().resolve()
    path = Path(home, folder)
    Path(path).mkdir(parents=True, exist_ok=True)
    file_name = urlsplit(url)[2].split('/')[-1]
    named_path = f'{path}/{file_name}'
    r = requests.get(url)
    r.raise_for_status()
    with open(named_path, 'wb') as file:
        file.write(r.content)


if __name__=='__main__':
    url = 'https://api.spacexdata.com/v4/launches/5eb87d42ffd86e000604b384'
    r = requests.get(url)
    api_r = r.json()
    images_urls = api_r.get('links').get('flickr').get('original')
    folder = 'images'
    for img_url in images_urls:
        download_image(img_url, folder)