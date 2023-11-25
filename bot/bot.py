import json
import random
import string
from copy import copy

import requests


class Bot:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.users = []
        self.post_ids = []
        self.host = "http://127.0.0.1:80/api/"
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

    @staticmethod
    def pop_random_value(my_list):
        if not my_list:
            return None  # Return None if the list is empty

        random_index = random.randrange(len(my_list))
        return my_list.pop(random_index)

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            return json.load(file)

    def signup_users(self):
        url = self.host + 'user/signup'
        token = self.token

        # Include the Bearer token in the headers
        headers = {"Authorization": f"Bearer {token}"}

        for user in range(self.config['number_of_users']):
            # Choose a random username of length 8
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

            # Choose a random domain from a list
            domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'example.com', 'mail.com']
            domain = random.choice(domains)

            # Combine username and domain to create the email address
            email = f"{username}@{domain}"

            user = {
                'email': email,
                'password': 'testtest'
            }
            response = requests.post(url, json=user, headers=headers)
            if response.status_code == 200:
                self.users.append(user)

    def signin_users(self):
        url = self.host + 'user/signin'
        token = self.token

        # Include the Bearer token in the headers
        headers = {"Authorization": f"Bearer {token}"}

        for user in self.users:
            response = requests.post(url, json=user, headers=headers)
            if response.status_code == 200:
                user['token'] = response.json().get('access_token')

    def create_posts(self):
        url = self.host + 'post'
        max_posts_per_user = self.config['max_posts_per_user']
        for user in self.users:
            headers = {"Authorization": f"Bearer {user.get('token')}"}

            number_of_posts = random.randrange(max_posts_per_user)
            print(f'user {user.get("email")} will send {number_of_posts} posts')
            for post_number in range(number_of_posts):
                letters = string.ascii_letters + string.digits + string.punctuation + string.whitespace
                text = ''.join(random.choice(letters) for _ in range(30))

                payload = {
                    "content": text
                }

                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    print(f'post {post_number} of user {user.get("email")} created successfully')
                    post_id = response.json().get('post_id')
                    self.post_ids.append(post_id)

    def like_posts(self):
        url = self.host + 'post/assess/'
        max_likes_per_user = self.config['max_likes_per_user']
        for user in self.users:
            headers = {"Authorization": f"Bearer {user.get('token')}"}

            number_of_likes = random.randrange(max_likes_per_user)
            print(f'user {user.get("email")} will send {number_of_likes} likes')

            if number_of_likes > len(self.post_ids):
                number_of_likes = self.post_ids

            for like_number in range(number_of_likes):
                post_ids = copy(self.post_ids)
                random_post_id = self.pop_random_value(post_ids)

                payload = {
                    "post_id": random_post_id,
                    "like": True
                }

                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200 or response.status_code == 201:
                    print(f'post id {random_post_id} liked successfully')


if __name__ == "__main__":
    bot = Bot("config.json")

    bot.signup_users()
    bot.signin_users()
    bot.create_posts()
    bot.like_posts()
