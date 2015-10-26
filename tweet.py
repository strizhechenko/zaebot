# coding: utf-8
import sys
from tweepy import OAuthHandler, API, TweepError
from ConfigParser import ConfigParser


class Twibot():

    def conf2api(self, config='config.ini', user='writer'):
        with open(config) as f:
            c = ConfigParser()
            c.readfp(f)
        app = dict(c.items('app'))
        user = dict(c.items(user))
        auth = OAuthHandler(app['consumer_key'], app['consumer_secret'])
        auth.set_access_token(user['access_token'], user['access_secret'])
        return API(auth)

    def __init__(self, user='writer'):
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
            except TweepError as err:
                print 'Duplicate or error', err
        return False


if __name__ == '__main__':
    TwibotWriter().tweet(" ".join(sys.argv[1:]))
