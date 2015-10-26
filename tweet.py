#!/usr/bin/python

# coding: utf-8
import os
import tweepy
import threading
import sys
from ConfigParser import ConfigParser


class Twibot(threading.Thread):

    def conf2api(self, config='config.ini', user='writer'):
        with open(config) as f:
            c = ConfigParser()
            c.readfp(f)
        app = dict(c.items('app'))
        user = dict(c.items(user))
        auth = tweepy.OAuthHandler(app['consumer_key'], app['consumer_secret'])
        auth.set_access_token(user['access_token'], user[
                              'access_token_secret'])
        return tweepy.API(auth)

    def __init__(self, user='writer'):
        threading.Thread.__init__(self)
        self.api = self.conf2api(user=user)

class TwibotReader(Twibot):
    def fetch(self, count=3):
        return self.api.home_timeline(count)


class TwibotWriter(Twibot):
    def tweet(self, tweet):
        if len(tweet) <= 140 and len(tweet) > 0:
            try:
                self.api.update_status(tweet)
                return True
            except tweepy.TweepError as err:
                print 'Duplicate or error', err
        return False


if __name__ == '__main__':
    TwibotWriter().tweet(" ".join(sys.argv[1:]))
