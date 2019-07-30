import json

import faker
from requests import Session


class ApiClient:
    def __init__(self):
        self.session = Session()
        self.fake = faker.Faker()

    def signup(self) -> dict:
        """
        Signup new user.
        """
        password = self.fake.password()
        user_data = self.session.put(
            url='http://127.0.0.1:8000/api/v1/auth/signup',
            json={
                'username': self.fake.profile(fields='username')['username'],
                'email': self.fake.email(),
                'password': password,
            }).content

        user_data = json.loads(user_data)

        user_data['password'] = password
        user_data['likes'] = 0

        return user_data

    def login(self, user) -> str:
        """
        Perform login and returns access token.
        """
        response_data = json.loads(self.session.post(
            url='http://127.0.0.1:8000/api/v1/auth/login',
            json={
                'username': user.get('username'),
                'password': user.get('password'),
            },
        ).content)
        access_token = response_data['access']
        return access_token

    def create_random_post(self):
        """
        Create post with random content and return its id.
        """
        response_data = json.loads(self.session.put(
            url='http://127.0.0.1:8000/api/v1/post/',
            json={
                'title': self.fake.name(),
                'text': self.fake.text(),
            },
        ).content)
        response_data['liked'] = False
        return response_data

    def like(self, post) -> dict:
        """
        Put a like on post.
        """
        response = self.session.put(
            url=f"http://127.0.0.1:8000/api/v1/post/{post['id']}/likes/",
        )
        response_data = json.loads(response.content)
        print(response_data)
        return response_data

    def change_current_user(self, user):
        access_token = self.login(user)
        self.session.headers.update({'Authorization': f'Bearer {access_token}'})