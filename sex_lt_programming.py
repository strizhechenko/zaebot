# coding: utf-8
from bot import Zaebot
x = Zaebot()

phrase = u'ебаться надо'
phrase_correct = lambda tweet: phrase in tweet
not_hashtag_or_reply = lambda tweet: u'@' not in tweet and u'#' not in tweet
tweet_to_text = lambda tweet: tweet.text.lower()

tweets = x.reader.api.search(phrase, count=200)
tweets_text = map(tweet_to_text, tweets)
tweets_text = filter(not_hashtag_or_reply, filter(phrase_correct, tweets_text))

for i in tweets_text:
    print i.replace(u'ебаться', u'программировать').encode('utf-8')
