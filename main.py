import requests
import os

from random import randint
from dotenv import load_dotenv



def fetch_image(filename, url):
    path = os.getcwd()
    response = requests.get(url)
    response.raise_for_status()
    with open(os.path.join(path,filename), 'wb') as file:
        file.write(response.content)


def get_xkcd_last_comics_number():
    url = 'http://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['num']


def fetch_random_xkcd_comics(last_comics_number):
    url = 'http://xkcd.com/{}/info.0.json'.format(randint(0,last_comics_number))
    response = requests.get(url)
    response.raise_for_status()
    filename = response.json()['img'].split('/')[-1]
    alt_description = response.json()['alt']
    fetch_image(filename, response.json()['img'])
    return filename, alt_description


def main(group_id, access_token):
    image, message = fetch_random_xkcd_comics(get_xkcd_last_comics_number())
    upload_url = get_wall_upload_server(group_id,
                                        access_token)['response']['upload_url']
    server_response = upload_photo_to_server(group_id, image, upload_url)
    saved_image_params = save_photo_to_wall(group_id,
                                            access_token,
                                            server_response)
    post_photo_to_wall(group_id, access_token, saved_image_params, message)
    os.remove(image)


def get_wall_upload_server(group_id, access_token):
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'v': 5.95,
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params)
    return response.json()


def upload_photo_to_server(group_id, photo, upload_url):
    with open(photo, 'rb') as image_file_descriptor:
        response = requests.post(upload_url,
                                 params={'group_id': group_id},
                                 files={'photo': image_file_descriptor})
    return response.json()


def save_photo_to_wall(group_id, access_token, uploading_response):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': xkcd_group_id,
        'access_token': access_token,
        'v': 5.95,
        'hash': uploading_response['hash'],
        'photo': uploading_response['photo'],
        'server': uploading_response['server'],
    }
    response = requests.post(url, params)
    return response.json()


def post_photo_to_wall(group_id, access_token, saved_image_params, message):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': access_token,
        'v': 5.95,
        'owner_id': group_id*-1,
        'from_group': 1,
        'attachments':'photo{}_{}'.format(
            saved_image_params['response'][0]['owner_id'],
            saved_image_params['response'][0]['id']),
        'message': message,
    }
    requests.post(url, params)


if __name__=='__main__':
    load_dotenv()
    access_token = os.getenv('access_token')
    group_id = 181988331
    image, message = fetch_random_xkcd_comics(get_xkcd_last_comics_number())
    upload_url = get_wall_upload_server(group_id,
                                        access_token)['response']['upload_url']
    server_response = upload_photo_to_server(group_id, image, upload_url)
    saved_image_params = save_photo_to_wall(group_id,
                                            access_token,
                                            server_response)
    post_photo_to_wall(group_id, access_token, saved_image_params, message)
    os.remove(image)

