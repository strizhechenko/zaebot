# coding: utf-8
from pymorphy2 import MorphAnalyzer
import re
from random import shuffle


class Morpher(MorphAnalyzer):

    def __init__(self):
        super(Morpher, self).__init__()
        self.parsed_zaeb = self.parse(u'заебать')[0]

    def nouns(self, words):
        is_noun = lambda w: not [
            i for i in self.parse(w) if 'NOUN' not in i.tag]
        return filter(is_noun, words)

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
        if gender in ('neut', 'femn', 'masc'):
            return self.parsed_zaeb.inflect(set([gender])).word
        return u'Заебись'

    def ru_only(self, string):
        return set(map(unicode.lower, re.findall(u'[А-Яа-я]+', string)))

    def process_to_words(self, string):
        words = self.nouns(self.ru_only(string))
        normal_words = map(self.normalize_word, words)
        shuffle(normal_words)
        return normal_words[:3]

    def word2phrase(self, word):
        return "%s %s" % (self.zaeb(word), word)
