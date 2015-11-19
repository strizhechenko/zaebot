# coding: utf-8
""" раз в час пытаемся запостить цитатку про то как надо программировать """

from apscheduler.schedulers.blocking import BlockingScheduler
from bot import Zaebot
from hashlib import md5

bot = Zaebot()
sched = BlockingScheduler()

phrase = u'ебаться надо'
replacement = u'программировать надо'
phrase_correct = lambda tweet: phrase in tweet
not_hashtag_or_reply = lambda tweet: u'@' not in tweet and u'#' not in tweet
tweet_to_text = lambda tweet: tweet.text.lower()
hasher = md5()

def get_hashes():
    hashes = []
    me = bot.writer.api.me()
    timeline = me.timeline(count=200)
    for tweet in [t.text for t in timeline]:
        hasher.update(tweet.encode('utf-8'))
        hashes.append(hasher.hexdigest())
    return list(set(hashes))

@sched.scheduled_job('interval', minutes=60)
def do_tweets():
    hashes = get_hashes()
    tweets = bot.reader.api.search(phrase, count=200)
    tweets_text = map(tweet_to_text, tweets)
    tweets_text = filter(phrase_correct, tweets_text)
    tweets_text = filter(not_hashtag_or_reply, tweets_text)

    for tweet in tweets_text:
        tweet_text = tweet.replace(phrase, replacement).encode('utf-8')
        print 'checking', tweet_text
        hasher.update(tweet_text)
        if hasher.hexdigest() not in hashes:
            print 'not posted before'
            bot.writer.tweet(tweet_text)

sched.start()
