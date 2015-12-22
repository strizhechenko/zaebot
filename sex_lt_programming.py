# coding: utf-8
""" раз в час пытаемся запостить цитатку про то как надо программировать """

from apscheduler.schedulers.blocking import BlockingScheduler
from tweet import Twibot
from hashlib import md5
from time import sleep
import sys

bot = Twibot()
sched = BlockingScheduler()

not_hashtag_or_reply = lambda tweet: u'@' not in tweet and u'#' not in tweet
tweet_to_text = lambda tweet: tweet.text.lower()
hashes = []

blacklist = (
    u'выпущено 24 кролика',
    u'учёные выяснили',
    u'ученые выяснили',
    u'учёные узнали',
    u'ученые узнали',
    u'как часто',
    u'психологи узнали',
    u'психологи выяснили',
    u'http://',
    u'https://',
    u'.com',
    u't.co',
)

replacements = {
    u'ебутся': {
        u'ебутся': u'программируют',
    },
    u'ебаться': {
        u'ебаться': u'программировать',
    },
    u'трахаться': {
        u'трахаться': u'программировать',
    },
    u'в сексе главное': {
        u'сексе':   u'программировании',
    },
    u'заниматься сексом': {
        u'заниматься сексом': u'программировать',
        u'сексом заниматься': u'программировать',
    },
    u'покажите сиськи': {
        u'покажите': u'откройте',
        u'сиськи': u'исходники',
    },
}

def not_blacklisted(tweet):
    for phrase in blacklist:
        if phrase in tweet:
            return False
    return True

def get_hashes():
    """ хэшики последних 200 своих твитов """
    hashes = []
    me = bot.api.me()
    timeline = me.timeline(count=200)
    for tweet in [t.text for t in timeline]:
        hashes.append(md5(tweet.encode('utf-8')).hexdigest())
    return list(set(hashes))


def process_tweet(tweet, replaces, hashes):
    """ обрабатываем полученные твиты и постим новые """
    tweet_original = tweet
    for word, replace in replaces.items():
        tweet = tweet.replace(word, replace)
    if tweet_original == tweet:
        return
    if len(tweet) > 140:
        if isinstance(tweet, unicode):
            tweet = tweet.encode('utf-8')
        print 'too long :( :', tweet
        return
    tweet = tweet.encode('utf-8')
    tweet_hash = md5(tweet).hexdigest()
    if tweet_hash in hashes:
        return
    bot.tweet(tweet)


@sched.scheduled_job('interval', minutes=15)
def do_tweets():
    """ тянем нужные твиты и скармливаем постилке """
    hashes.extend(get_hashes())
    for phrase, replaces in replacements.items():
        sleep(60)
        print '# search:', phrase.encode('utf-8')
        tweets = bot.api.search(phrase, count=200, result_type='recent')
        tweets_text = map(tweet_to_text, tweets)
        tweets_text = filter(not_hashtag_or_reply, tweets_text)
        tweets_text = filter(not_blacklisted, tweets_text)
        for tweet in tweets_text:
            process_tweet(tweet, replaces, hashes)
            sleep(2)


if __name__ == '__main__':
    do_tweets()
    if '--test' in sys.argv:
        do_tweets()
        exit(0)
    sched.start()
