# coding: utf-8
__author__ = "@strizhechenko"

import sys

from morpher import Morpher
from twitterbot_utils import Twibot
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
bot = Twibot()
morphy = Morpher()


def tweets2words(tweets):
    string = " ".join([tweet.text for tweet in tweets])
    return morphy.process_to_words(string)


@sched.scheduled_job('interval', minutes=15)
def do_tweets():
    print 'New tick'
    words = tweets2words(bot.fetch_list(list_id=217926157))
    for word in words:
        tweet = morphy.word2phrase(word)
        bot.tweet(tweet)
        print 'post', tweet.encode('utf-8')


@sched.scheduled_job('interval', hours=24)
def do_wipe():
    print 'Wipe time'
    bot.wipe()

if __name__ == '__main__':
    do_tweets()
    if '--test' in sys.argv:
        exit(0)
    sched.start()
