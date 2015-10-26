# coding: utf-8

__author__ = "@strizhechenko"

import time
from random import randint
from tweet import TwibotWriter, TwibotReader
from morpher import Morpher


class Zaebot():

    def __init__(self):
        self.writer = TwibotWriter(user='writer')
        self.reader = TwibotReader(user='reader')
        self.morph = Morpher()

    def get_words(self):
        string = " ".join(map(lambda tw: tw.text, self.reader.fetch()))
        return self.morph.process_to_words(string)

    def loop(self):
        while True:
            for word in self.get_words():
                self.writer.tweet(self.morph.word2phrase(word))
            time.sleep(randint(1, 2) * 60)

if __name__ == '__main__':
    bot = Zaebot()
    bot.loop()
