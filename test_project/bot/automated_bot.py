import random

import utils
from bot.bot_client_api import ApiClient


class AutomatedBot:

    def __init__(self, number_of_users):
        self.api = ApiClient()
        self.users = [user for user in self.signup_random_users(number_of_users)]
        self.posts = []

    def signup_random_users(self, count):
        for i in range(count):
            yield self.api.signup()

    def create_random_posts(self, max_posts_per_user):
        """
        Create random count (up to max_posts_per_user) of posts with random content.
        """
        for user in self.users:
            user['posts'] = 0
            self.api.change_current_user(user)

            for i in range(random.randrange(max_posts_per_user)):
                post = self.api.create_random_post()
                self.posts.append(post)
                user['posts'] += 1

    def _get_next_user_for_liking(self, max_likes_per_user):
        """
        Return user that put likes less than max amount and has the biggest amount of posts.
        """
        sorted(self.users, key=lambda x: x['posts'], reverse=True)
        for user in self.users:
            if user['likes'] <= max_likes_per_user:
                return user

    def put_likes(self, max_likes_per_user):
        """
        Put up to max amount of likes to random posts from users who have post with 0 likes until he reaches max likes.
        If there is no posts with 0 likes, bot stops.
        Users cannot like their own posts.
        Posts can be liked multiple times, but one user can like a certain post only once.
        """

        while True:
            user = self._get_next_user_for_liking(max_likes_per_user)
            self.api.change_current_user(user)
            if not user:
                return

            while user['likes'] <= max_likes_per_user:

                unliked_posts = list(filter(lambda post: not post['liked'], self.posts))
                unliked_users = set(post['user'] for post in unliked_posts)
                possible_posts = list(
                    filter(
                        lambda post: post['user'] in unliked_users
                                     and post['user'] != user['username']
                                     and not post['liked'],
                        self.posts
                    )
                )

                if not unliked_posts:
                    return
                if not possible_posts:
                    break

                post = random.choice(possible_posts)
                self.api.like(post)
                post['liked'] = True
                user['likes'] += 1


if __name__ == '__main__':
    number_of_users, max_posts_per_user, max_likes_per_user = utils.get_config_params()

    bot = AutomatedBot(number_of_users)
    bot.create_random_posts(max_posts_per_user)
    bot.put_likes(max_likes_per_user)
