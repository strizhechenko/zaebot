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


@sched.scheduled_job('interval', minutes=15)
def do_tweets():
    tweets = reader.api.home_timeline(count=3)
    string = " ".join([tweet.text for tweet in tweets])
    words = morphy.process_to_words(string)
    for word in words:
        tweet = morphy.word2phrase(word)
        bot.tweet(tweet)


@sched.scheduled_job('interval', hours=24)
def do_wipe():
    bot.wipe()

if __name__ == '__main__':
    if '--test' in sys.argv:
        do_tweets()
        exit(0)
    sched.start()
