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

    def __get_words__(self):
        tweets = self.reader.fetch()
        string = " ".join([ tweet.text for tweet in tweets ])
        return self.morphy.process_to_words(string)

    def loop(self):
        tweet_count = 0
        while True:
            for word in self.__get_words__():
                self.writer.tweet(self.morphy.word2phrase(word))
                tweet_count+=1
            if tweet_count > 100:
                tweet_count = 0
                self.writer.wipe()
            sleep(randint(15, 30) * randint(30, 60))

if __name__ == '__main__':
    Zaebot().loop()
