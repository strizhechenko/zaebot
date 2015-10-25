# coding: utf-8

__author__ = "@strizhechenko"

import re, time
from random import shuffle, randint
from tweet import TwiBot
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
parsed_zaeb = morph.parse(u'заебать')[0]


def fetch_tweet_words(user):
    text = lambda tweet: tweet.text
    tweets = user.api.home_timeline(count=3)
    string = " ".join(map(text, tweets))
    return set(map(unicode.lower, re.findall(u'[А-Яа-я]+', string)))


def nouns(words):
    is_noun = lambda w: not [i for i in morph.parse(w) if 'NOUN' not in i.tag]
    return filter(is_noun, words)


def normalize_word(word):
    parsed = morph.parse(word)
    single = lambda w: 'sing' in w.tag or 'Sgtm' in w.tag
    if any(map(single, parsed)):
        return filter(single, parsed)[0].normal_form
    return parsed[0].normal_form


def zaeb(word):
    w = morph.parse(word)[0]
    gender = w.tag.gender
    if w.tag.number == 'plur':
        return u'Заебали'
    if gender in ('neut', 'femn', 'masc'):
        return parsed_zaeb.inflect(set([gender])).word
    return u'Заебись'
    

def get_words(reader):
    words = map(normalize_word, (nouns(fetch_tweet_words(reader))))
    shuffle(words)
    return words[:3]


if __name__ == '__main__':
    writer = TwiBot(user='twibot')
    reader = TwiBot(user='grabber')
    while True:
        for word in get_words(reader):
            writer.tweet(tweet_text = "%s %s" % (zaeb(word), word))
        time.sleep(randint(1, 60) * 60)        
