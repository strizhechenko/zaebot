# coding: utf-8
""" раз в час пытаемся запостить цитатку про то как надо программировать """

from apscheduler.schedulers.blocking import BlockingScheduler
from tweet import Twibot
from hashlib import md5
import sys

bot = Twibot()
sched = BlockingScheduler()
hasher = md5()

not_hashtag_or_reply = lambda tweet: u'@' not in tweet and u'#' not in tweet
tweet_to_text = lambda tweet: tweet.text.lower()

replacements = {
    u'ебаться надо': {
        u'ебаться': u'программировать',
    },
    u'в сексе главное': {
        u'сексе':   u'программировании',
    },
    u'трахаться надо': {
        u'трахаться': u'программировать',
    },
    u'заниматься сексом надо': {
        u'заниматься сексом': u'программировать',
        u'сексом заниматься': u'программировать',
    },
    u'ебаться в жопу': {
        u'ебаться': u'пушить',
        u'в жопу': u'с форсом',
    },
}


def get_hashes():
    """ хэшики последних 200 своих твитов """
    hashes = []
    me = bot.api.me()
    timeline = me.timeline(count=200)
    for tweet in [t.text for t in timeline]:
        hasher.update(tweet.encode('utf-8'))
        hashes.append(hasher.hexdigest())
    return list(set(hashes))


def process_tweet(tweet, replaces, hashes):
    """ обрабатываем полученные твиты и постим новые """
    for word, replace in replaces.items():
        tweet = tweet.replace(word, replace)
    tweet = tweet.encode('utf-8')
    hasher.update(tweet)
    if hasher.hexdigest() in hashes:
        return
    bot.tweet(tweet)


@sched.scheduled_job('interval', minutes=60)
def do_tweets():
    """ тянем нужные твиты и скармливаем постилке """
    hashes = get_hashes()
    for phrase, replaces in replacements.items():
        print phrase.encode('utf-8')
        tweets = bot.api.search(phrase, count=10)
        tweets_text = map(tweet_to_text, tweets)
        tweets_text = filter(not_hashtag_or_reply, tweets_text)
        for tweet in tweets_text:
            process_tweet(tweet, replaces, hashes)


if __name__ == '__main__':
    if '--test' in sys.argv:
        do_tweets()
    else:
        sched.start()
