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
timeout = int(os.environ.get('timeout', 30))
template = unicode(os.environ.get('template', u''), 'utf-8')
tweet_grab = int(os.environ.get('tweet_grab', 3))
tweets_per_tick = int(os.environ.get('tweets_per_tick', 2))

@sched.scheduled_job('interval', minutes=timeout)
def do_tweets():
    print 'New tick'
    tweets = reader.api.home_timeline(count=tweet_grab)
    string = " ".join([tweet.text for tweet in tweets])
    words = morphy.process_to_words(string, count=tweets_per_tick)
    posts = [template % (word) for word in words]
    bot.tweet_multiple(posts, logging=True)
    print 'Wait for', timeout, 'minutes'


if __name__ == '__main__':
    do_tweets()
    if '--test' in sys.argv:
        exit(0)
    sched.start()
