# coding: utf-8
from pymorphy2 import MorphAnalyzer
import re
from random import shuffle


class Morpher(MorphAnalyzer):

    def __init__(self):
        super(Morpher, self).__init__()
        self.zaebat = self.parse(u'заебать')[0]
        self.genders = ('neut', 'femn', 'masc')

    def is_noun(self, word):
        for w in self.parse(word):
            if 'NOUN' not in w.tag:
                return False
        return True

    def normalize_word(self, word):
        parsed = self.parse(word)
        single = lambda w: 'sing' in w.tag or 'Sgtm' in w.tag
        if any(map(single, parsed)):
            return filter(single, parsed)[0].normal_form
        return parsed[0].normal_form

    def zaeb(self, word):
        w = self.parse(word)[0]
        gender = w.tag.gender
        if w.tag.number == 'plur':
            return u'Заебали'
        if gender in self.genders:
            return self.zaebat.inflect(set([gender])).word
        return u'Заебись'

    @staticmethod
    def ru_only(string):
        return set(map(unicode.lower, re.findall(u'[А-Яа-я]+', string)))

    def process_to_words(self, string, count=1):
        words = filter(self.is_noun, self.ru_only(string))
        normal_words = map(self.normalize_word, words)
        shuffle(normal_words)
        return normal_words[:count]

    def word2phrase(self, word):
        return "%s %s" % (self.zaeb(word), word)
