# coding: utf-8

from apscheduler.schedulers.blocking import BlockingScheduler
from bot import Zaebot

bot = Zaebot()
sched = BlockingScheduler()

phrase = u'ебаться надо'
replacement = u'программировать надо'
phrase_correct = lambda tweet: phrase in tweet
not_hashtag_or_reply = lambda tweet: u'@' not in tweet and u'#' not in tweet
tweet_to_text = lambda tweet: tweet.text.lower()

# @sched.scheduled_job('interval', minutes=60)
def do_tweets():
    tweets = bot.reader.api.search(phrase, count=200)
    tweets_text = map(tweet_to_text, tweets)
    tweets_text = filter(phrase_correct, tweets_text)
    tweets_text = filter(not_hashtag_or_reply, tweets_text)

    for tweet in tweets_text:
        tweet_text = tweet.replace(phrase, replacement).encode('utf-8')
        bot.writer.tweet(tweet_text)

# sched.start()
do_tweets()
