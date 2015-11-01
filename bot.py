# coding: utf-8
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

    def get_words(self, count=1):
        tweets = self.reader.fetch(count=100)
        string = " ".join([tweet.text for tweet in tweets])
        return self.morphy.process_to_words(string, count)

    def loop_body(self):
        words1 = self.get_words(200)
        words2 = self.get_words(200)
        # self.writer.tweet(self.morphy.word2phrase(word))
        for i in xrange(150):
            print ("%s-%s %s" % ( words1[i], words2[i], u'из открытого космоса' )).encode('utf-8')
        # self,morphy.word2phrase(word)


    def loop(self):
        tweet_count = 0
        while True:
            self.loop_body()
            tweet_count+=1
            if tweet_count > 100:
                tweet_count = 0
                self.writer.wipe()
            sleep(randint(15, 30) * randint(30, 60))

if __name__ == '__main__':
    Zaebot().loop_body()
