import requests
import json
import csv
from time import sleep
from datetime import datetime


class parse_request:
    '''
    second Part Creating posts graph in the group
    '''
    def __init__(self, token):
        self.token = token
        
    def get_posts(self, owner_id): # Second Part Main method
        choice = 'owner_id' if type(owner_id) != type('') else 'domain'
        posts = []
        version = 5.21
        count = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': self.token,
                                'v': version,
                                'type': 'post',
                                choice: owner_id,
                                'count': 1,
                                'offset': 0}).json()['response']['count']//100
        i = 0
        while i <= count:
            posts_info = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': self.token,
                                'v': version,
                                'type': 'post',
                                choice: owner_id,
                                'count': 100,
                                'offset': 100*i}).json()['response']
            hundred_items = []
            for post_info in posts_info['items']:
                if post_info['post_type'] == 'post':
                    list_of_liked_users = self.__get_posts_likes(post_info['id'], post_info['owner_id'])
                    hundred_items.append((post_info['id'], {'count': len(list_of_liked_users), 'users': list_of_liked_users}))
            posts += hundred_items
            i += 1
        return posts

    def __get_posts_likes(self, item_id, owner_id):
        group_posts_likes = []
        version = 5.21
        count = requests.get('https://api.vk.com/method/likes.getList',
                            params={
                                'access_token': self.token,
                                'v': version,
                                'type': 'post',
                                'owner_id': owner_id,
                                'item_id': item_id,
                                'count': 100,
                                'offset': 0}).json()['response']['count']//100
        i = 0
        while i <= count:
            post_info = requests.get('https://api.vk.com/method/likes.getList',
                                    params={
                                        'access_token': self.token,
                                        'v': version,
                                        'type': 'post',
                                        'owner_id': owner_id,
                                        'item_id': item_id,
                                        'count': 100,
                                        'offset': 100*i}).json()['response']
            group_posts_likes += post_info['items']
            i += 1
        return group_posts_likes


    '''
    Third Part Creating friends graph
    '''
    def get_users(self, list_of_user): # Third Part Main method
        users = []
        for user in list_of_user:
            try:
                users.append(self.__get_user_friends(user))
            except:
                pass
        return users
    
    def __get_user_friends(self, user_id): # friends.get
        user_friends = []
        version = 5.21

        user = requests.get('https://api.vk.com/method/users.get',
                            params={
                                'access_token': self.token,
                                'v': version,
                                'user_ids': user_id}).json()['response'][0]

        count = requests.get('https://api.vk.com/method/friends.get',
                            params={
                                'access_token': self.token,
                                'v': version,
                                'user_id': user['id'],
                                'fields': 'id',
                                'count': 1
                                }).json()['response']['count']//5000
        i = 0
        while i <= count:
            friend_info = requests.get('https://api.vk.com/method/friends.get',
                                    params={
                                        'access_token': self.token,
                                        'v': version,
                                        'user_id': user['id'],
                                        'count': 5000,
                                        'offset': 5000*i}).json()['response']
            user_friends += friend_info['items']
            i += 1
        return (user['first_name']+' '+user['last_name'], {'count': len(user_friends), 'users': user_friends})