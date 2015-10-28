__author__ = "@strizhechenko"

from time import sleep
from random import randint
from tweet import TwibotWriter, TwibotReader
from morpher import Morpher


class Zaebot():

    def __init__(self):
        self.writer = TwibotWriter(user='writer')
        self.reader = TwibotReader(user='reader')
        self.morphy = Morpher()

    def tweets2words(self, tweets):
        string = " ".join([tweet.text for tweet in tweets])
        return self.morphy.process_to_words(string)

    def home_timeline_words(self):
        tweets = self.reader.fetch()
        return self.tweets2words(tweets)

    def list_words(self, list_id):
        tweets = self.reader.fetch_list(list_id)
        return self.tweets2words(tweets)

    def loop(self):
        tweet_count = 0
        while True:
            # for word in self.home_timeline_words():
            for word in self.list_words(list_id = 217926157):
                self.writer.tweet(self.morphy.word2phrase(word))
                tweet_count += 1
            if tweet_count > 100:
                tweet_count = 0
                self.writer.wipe()
            sleep(randint(15, 30) * randint(30, 60))

if __name__ == '__main__':
    Zaebot().loop()
