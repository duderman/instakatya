# -*- coding: utf-8 -*-

from glob import glob
import os
import sys
import threading
import time

sys.path.append(os.path.join(sys.path[0], '../../'))
import schedule
from instabot import Bot, utils

bot = Bot()
bot.login()

def stats():
    bot.save_user_stats(bot.user_id)

def follow():

def like():

def rotate_followed():

def unfollow_old():



def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


schedule.every(1).hour.do(run_threaded, stats)
schedule.every(1).hour.do(run_threaded, follow)
schedule.every(1).hour.do(run_threaded, like)
schedule.every(1).days.at("07:00").do(run_threaded, rotate_followed)
schedule.every(1).days.at("08:00").do(run_threaded, unfollow_old)

while True:
    schedule.run_pending()
    time.sleep(1)
