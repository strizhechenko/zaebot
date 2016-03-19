# coding: utf-8

"""
Бот, собирает существительные из ленты одного пользователя, подставляет их в
шаблон из environ и постит несколько твитов
"""

import sys
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from twitterbot_utils import Twibot, get_maximum_tweets
from morpher import Morpher

__author__ = "@strizhechenko"

SCHED = BlockingScheduler()
BOT = Twibot()
READER = Twibot(username=os.environ.get('reader_name'))
MORPHY = Morpher()
TIMEOUT = int(os.environ.get('timeout', 30))
TEMPLATE = unicode(os.environ.get('template', u''), 'utf-8')
TWEET_GRAB = int(os.environ.get('tweet_grab', 3))
TWEETS_PER_TICK = int(os.environ.get('tweets_per_tick', 2))
POSTED = get_maximum_tweets(BOT.api.home_timeline)


@SCHED.scheduled_job('interval', minutes=TIMEOUT)
def do_tweets():
    """ периодические генерация и постинг твитов """
    print 'New tick'
    tweets = READER.api.home_timeline(count=TWEET_GRAB)
    string = " ".join([tweet.text for tweet in tweets])
    words = MORPHY.process_to_words(string, count=TWEETS_PER_TICK)
    posts = [TEMPLATE % (word) for word in words]
    posts = [post for post in posts if post not in POSTED]
    BOT.tweet_multiple(posts, logging=True)
    POSTED.extend(posts)
    print 'Wait for', TIMEOUT, 'minutes'


if __name__ == '__main__':
    if '--wipe' in sys.argv:
        BOT.wipe()
        exit(0)
    do_tweets()
    if '--test' in sys.argv:
        exit(0)
    SCHED.start()
