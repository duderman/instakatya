# -*- coding: utf-8 -*-

from glob import glob
import os
import sys
import threading
import time
import schedule
import random
from instabot import Bot, utils

import config
import credentials

MAX = 99999

bot = Bot(
    max_follows_per_day=350,
    max_unfollows_per_day=350,
    max_likes_to_like=100,
    min_likes_to_like=0,
    filter_private_users=False,
    filter_users_without_profile_photo=True,
    filter_previously_followed=True,
    filter_business_accounts=False,
    max_followers_to_follow=config.MAX,
    min_followers_to_follow=100,
    max_following_to_follow=config.MAX,
    min_following_to_follow=100,
    min_media_count_to_follow=10,
    like_delay=1,
    follow_delay=5,
    unfollow_delay=5
)
bot.login(username = credentials.USERNAME, password = credentials.PASSWORD)

def all_users():
    bot.read_list_from_file(config.USERS_FILE)

def random_user():
    random.choice(all_users())

def stats():
    bot.save_user_stats(bot.user_id)

def follow():
    bot.follow_followers(random_user(), nfollows = config.FOLLOW_COUNT)

def like():
    bot.like_followers(random_user(), nlikes=config.LIKES_COUNT)

# def rotate_followed():

# def unfollow_old():


def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


# schedule.every(1).hour.do(run_threaded, stats)
# schedule.every(1).hour.do(run_threaded, follow)
# schedule.every(1).hour.do(run_threaded, like)
# schedule.every(1).days.at("07:00").do(run_threaded, rotate_followed)
# schedule.every(1).days.at("08:00").do(run_threaded, unfollow_old)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

follow()
like()
stats()
