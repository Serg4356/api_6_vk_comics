import requests
import os

from dotenv import load_dotenv
from pprint import pprint



def fetch_image(filename, url):
    path = os.path.join(os.getcwd(), 'image')
    os.makedirs('image', exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(os.path.join(path,filename), 'wb') as file:
        file.write(response.content)


if __name__=='__main__':
    load_dotenv()
    app_id = os.getenv('APP_ID')
    access_token = os.getenv('access_token')
    url = 'https://api.vk.com/method/groups.get'
    xkcd_group_id = 181988331
    params = {
        'access_token': access_token,
        'v': 5.95,
    }
    #response = requests.get(url, params)
    #pprint(response.json())
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params['group_id'] = xkcd_group_id
    response = requests.get(url, params)
    pprint(response.json())
    upload_url = response.json()['response']['upload_url']
    #url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {}
    with open('./image/python.png', 'rb') as image_file_descriptor:
        #params['photo'] = image_file_descriptor
        response = requests.post(upload_url, files=image_file_descriptor)
    pprint(response.url)
    pprint(response.json())

    #url = 'http://xkcd.com/353/info.0.json'
    #response = requests.get(url)
    #pprint(response.json())
    #filename = response.json()['img'].split('/')[-1]
    #fetch_image(filename, response.json()['img'])
