# coding: utf-8
__author__ = "@strizhechenko"

import sys
import os

from morpher import Morpher
from twitterbot_utils import Twibot
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
bot = Twibot()
reader = Twibot(username=os.environ.get('reader_name'))
morphy = Morpher()


@sched.scheduled_job('interval', minutes=30)
def do_tweets():
    print 'New tick'
    tweets = reader.api.home_timeline(count=3)
    string = " ".join([tweet.text for tweet in tweets])
    words = morphy.process_to_words(string, count=2)
    posts = [u"%s - это когда тебя в жопу ебут." % (word) for word in words]
    bot.tweet_multiple(posts, logging=True)


if __name__ == '__main__':
    do_tweets()
    if '--test' in sys.argv:
        exit(0)
    sched.start()
