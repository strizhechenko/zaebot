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
        string = " ".join(map(lambda tweet: tweet.text, tweets))
        return self.morphy.process_to_words(string)

    def loop(self):
        while True:
            for word in self.__get_words__():
                self.writer.tweet(self.morphy.word2phrase(word))
            sleep(randint(15, 30) * randint(30, 60))

if __name__ == '__main__':
    Zaebot().loop()
