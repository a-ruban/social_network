import random
import string
from configparser import ConfigParser


def get_config_params():
    """
    Get params from config files.
    """
    config = ConfigParser()
    config.read('bot_config.ini')

    number_of_users = config['DEFAULT'].getint('number_of_users')
    max_posts_per_user = config['DEFAULT'].getint('max_posts_per_user')
    max_likes_per_user = config['DEFAULT'].getint('max_likes_per_user')
    return number_of_users, max_posts_per_user, max_likes_per_user
