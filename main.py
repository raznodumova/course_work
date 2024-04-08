import requests
import json
from pprint import pprint

TOKEN_YA = ''
TOKEN = ''

picture_dict = {}
photo_json = {}
photo_json_list = []


class VKapi:

    base_url = 'https://api.vk.ru/method'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.199'
        }

    def get_photos(self):
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile', 'extended': '1'})
        response = requests.get(f'{self.base_url}/photos.get', params=params).json()
        photos_items = response['response']['items']
        for item in photos_items:
            sizes = item['sizes']
            likes = item['likes']['count']
            date = item['date']
            max_height = 0

            for size in sizes:
                if size['height'] > max_height:
                    max_height = size['height']
                    if likes not in picture_dict.keys() and max_height == size['height']:
                        picture_dict[f'{likes}_{date}'] = size['url']
                        # photo_json = {}
                        photo_json['file_name'] = f'{likes}_{date}.jpg'
                        photo_json['size'] = size['type']

            photo_json_list.append(photo_json)
        with open('vk_image.json', 'w') as file:
            file.write(json.dumps(photo_json_list, ensure_ascii=True, indent=2))


class YD:
    base_url = 'https://cloud-api.yandex.net/'
    # path_ya = None

    def __init__(self, token):
        self.token = token

    def headers(self):
        return {
            'Authorization': self.token
        }

    def create_folder(self):

        params = {
            'path': 'VK_profile_photo'
        }
        response = requests.put(f'{self.base_url}v1/disk/resources', params=params, headers=self.headers())
        return response

    def upload_photos(self):
        for keys, values in picture_dict.items():
            upload_url = keys
            name_photo = values
            params = {
                'url': upload_url,
                'path': f"{self.create_folder()}/{name_photo}.jpg"
            }
            response = requests.post(f'{self.base_url}v1/disk/resources/upload', headers=self.headers(), params=params)


if __name__ == '__main__':
    vk_client = VKapi(TOKEN, 54733971)
    vk_client.get_photos()

    ya_client = YD(TOKEN_YA)
    ya_client.create_folder()
    ya_client.upload_photos()