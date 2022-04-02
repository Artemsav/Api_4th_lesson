import requests
import json

url = 'https://api.spacexdata.com/v4/launches/5eb87d42ffd86e000604b384'
payload = payload = {"text":'94'}
r = requests.get(url)
api_r = r.json()
print(api_r.get('links').get('flickr').get('original'))