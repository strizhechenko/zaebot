# coding: utf-8
__author__ = "@strizhechenko"

from time import sleep
from random import randint
from tweet import Twibot
from morpher import Morpher


class Zaebot():

    def __init__(self):
        self.bot = Twibot()
        self.morphy = Morpher()

    def __get_words__(self):
        tweets = self.bot.fetch(count=40)
        string = " ".join([tweet.text for tweet in tweets])
        print string.encode('utf-8')
        return self.morphy.process_to_words(string)

    def loop(self):
        tweet_count = 0
        while True:
            print u'Начало итерации'
            words = self.__get_words__()
            if not words:
                print u'Нет слов'
            for word in self.__get_words__():
                print u'Слово: ', word
                tweet = self.morphy.word2phrase(word)
                self.bot.tweet(tweet)
                tweet_count += 1
            if tweet_count > 100:
                tweet_count = 0
                self.bot.wipe()
            sleep(randint(15, 30) * randint(30, 60))

if __name__ == '__main__':
    Zaebot().loop()
