# coding: utf-8
""" раз в час пытаемся запостить цитатку про то как надо программировать """

from apscheduler.schedulers.blocking import BlockingScheduler
from tweet import Twibot
import tweepy
from hashlib import md5
from time import sleep
import sys
import re

bot = Twibot()
sched = BlockingScheduler()

not_hashtag_or_reply = lambda tweet: u'@' not in tweet and u'#' not in tweet
tweet_to_text = lambda tweet: tweet.text.lower()
hashes = []

blacklist = (
    u'выпущено 24 кролика', u'учёные выяснили', u'ученые выяснили',
    u'учёные узнали', u'ученые узнали', u'как часто',
    u'психологи узнали', u'психологи выяснили', u'http://',
    u'https://', u'.com', u't.co',
)

replacements = {
    u'ебутся': {u'ебутся': u'программируют', },
    u'ебаться': {u'ебаться': u'программировать', },
    u'трахаться': {u'трахаться': u'программировать', },
    u'в сексе главное': {u'сексе':   u'программировании', },
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
    """ некоторые твиты очень часто проскальзывают из-за модификаций """
    for phrase in blacklist:
        if phrase in tweet:
            return False
    return True


def get_hash(tweet):
    """ учитываем что люди тупые и часто немного меняют спизженный твит """
    return md5(re.sub('[ .,!?-]', '', tweet)).hexdigest()


def get_maximum_tweets():
    """ Тянем твитов сколько получится, чтобы не дублироваться """
    print "get_maximum_tweets..."
    tweets = []
    tweets_temp = bot.api.me().timeline(count=200)
    while tweets_temp:
        max_id = tweets_temp[-1].id - 1
        tweets.extend(map(lambda t: t.text, tweets_temp))
        print "200 more... now:", len(tweets)
        sleep(15)
        tweets_temp = bot.api.me().timeline(count=200, max_id=max_id)
    return list(set(tweets))


def get_hashes(tweets=None):
    """ хэшики последних 200 своих твитов """
    hashlist = []
    if not tweets:
        tweets = list(set(bot.api.me().timeline(count=200)))
    if not (tweets and isinstance(tweets, list)):
        return []
    if isinstance(tweets[0], tweepy.models.Status):
        hashlist.extend([get_hash(t.text.encode('utf-8')) for t in tweets])
    return list(set(hashlist))


def process_tweet(tweet, hashlist):
    """ обрабатываем полученные твиты и постим новые """
    replaced_tweet = tweet
    for replaces in replacements.values():
        for word, replace in replaces.items():
            replaced_tweet = replaced_tweet.replace(word, replace)
    if replaced_tweet == tweet:
        return
    if isinstance(replaced_tweet, unicode):
        replaced_tweet = replaced_tweet.encode('utf-8')
    if len(replaced_tweet) > 140 * 2 - 5:  # something wtf after encode
        print 'too long :( :', len(replaced_tweet), '__', replaced_tweet, '__'
        return
    if get_hash(replaced_tweet) in hashlist:
        return
    print 'post:', replaced_tweet
    bot.tweet(replaced_tweet)
    sleep(10)


@sched.scheduled_job('interval', minutes=30)
def do_tweets():
    """ тянем нужные твиты и скармливаем постилке """
    print "New tick, hashes before update:", len(hashes)
    hashes.extend(get_hashes())
    print "New tick, hashes after update:", len(hashes)
    for phrase in replacements.keys():
        sleep(10)
        print '# search:', phrase.encode('utf-8')
        tweets = bot.api.search(phrase, count=200, result_type='recent')
        tweets_text = map(tweet_to_text, tweets)
        tweets_text = filter(not_hashtag_or_reply, tweets_text)
        tweets_text = filter(not_blacklisted, tweets_text)
        for tweet in list(set(tweets_text)):
            process_tweet(tweet, hashes)
    print "Tick end, wait about 30 min"


if __name__ == '__main__':
    hashes.extend(get_hashes(tweets=get_maximum_tweets()))
    do_tweets()
    if '--test' in sys.argv:
        do_tweets()
        exit(0)
    sched.start()
