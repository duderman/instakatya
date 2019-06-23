# -*- coding: utf-8 -*-

from glob import glob
import os
import sys
import threading
import time
import schedule
import random
from instabot import Bot, utils
from datetime import datetime, timedelta

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
    unfollow_delay=5,
    max_followers_to_following_ratio=config.MAX,
    max_following_to_followers_ratio=config.MAX,
    base_path=config.BASE_PATH
)
bot.login(username = credentials.USERNAME, password = credentials.PASSWORD)

def file_path(filename):
    return  os.path.join(config.BASE_PATH, filename)

existing_followers = utils.file(config.EXISTING_FOLLOWERS_FILE)
processed_existing_followers = utils.file(file_path(config.PROCESSED_EXISTING_FOLLOWERS_FILE))

def all_users():
    return bot.read_list_from_file(config.USERS_FILE)

def random_user():
    return random.choice(all_users())

def followed_file_name(date):
    return file_path("followed_{}.txt".format(date.strftime("%Y%m%d")))

def today():
    return datetime.now()

def three_days_ago():
    return today() - timedelta(days = 3)

def save_to_followed_today(user_id):
    followed_today_file = utils.file(followed_file_name(today()))
    followed_today_file.append(user_id)

def follow_and_like(user_id):
    if not bot.follow(user_id):
        return False
    save_to_followed_today(user_id)
    bot.like_user(user_id, amount = config.LIKES_COUNT, filtration = False)
    return True

def random_followers():
    user = random_user()
    bot.logger.info("Getting random followers of {}".format(user))
    return bot.get_user_followers(random_user(), config.FOLLOWERS_COUNT)

def existing_followers_left():
    return list(set(existing_followers.list) - set(processed_existing_followers.list))

def random_existing_follower():
    return random.choice(existing_followers_left())

def next_existing_follower():
    follower = random_existing_follower()
    processed_existing_followers.append(follower)
    return follower

def process_followers():
    total_processed = 0

    for follower in random_followers():
        if follow_and_like(follower):
            total_processed += 1

    while total_processed < config.FOLLOWERS_COUNT:
        if follow_and_like(next_existing_follower()):
            total_processed += 1

def followed_3_days_ago():
    filename = followed_file_name(three_days_ago())
    return utils.file(filename).list

def unfollow_old():
    bot.unfollow_users(followed_3_days_ago())

def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


schedule.every(1).hour.do(run_threaded, process_followers)
schedule.every(1).days.at("08:00").do(run_threaded, unfollow_old)

while True:
    schedule.run_pending()
    time.sleep(1)
