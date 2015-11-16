# coding: utf-8
import os
import sys
from tweepy import OAuthHandler, API, TweepError
from ConfigParser import ConfigParser


class Twibot():

    @staticmethod
    def conf_dict_from_env(user='writer'):
        app = {
            'consumer_key': os.environ.get('consumer_key'),
            'consumer_secret': os.environ.get('consumer_secret'),
        }
        user = {
            'access_token': os.environ.get(user + '_access_token'),
            'access_secret': os.environ.get(user + '_access_secret'),
        }
        return app, user

    def conf_dict_from_config_file(self, config='config.ini', user='writer'):
        with open(config) as f:
            c = ConfigParser()
            c.readfp(f)
        app = dict(c.items('app'))
        user = dict(c.items(user))
        return app, user

    @staticmethod
    def conf_dict_to_api(app, user):
        auth = OAuthHandler(app['consumer_key'], app['consumer_secret'])
        auth.set_access_token(user['access_token'], user['access_secret'])
        return API(auth)

    def __init__(self, user='writer', config='env'):
        if config == 'env':
            app, user = self.conf_dict_from_env(user)
        else:
            app, user = self.conf_dict_from_config_file('config.ini', user)
        print app, user
        self.api = self.conf_dict_to_api(app, user)


class TwibotReader(Twibot):

    def fetch(self, count=3):
        return self.api.home_timeline(count=count)


class TwibotWriter(TwibotReader):

    def tweet(self, tweet):
        if len(tweet) <= 140 and len(tweet) > 0:
            try:
                self.api.update_status(tweet)
                return True
            except TweepError as err:
                print err
        return False

    def wipe(self):
        new_tweets = 30
        for tweet in self.fetch(200)[new_tweets:]:
            if tweet.favorite_count == 0 and tweet.retweet_count == 0:
                tweet.destroy()


if __name__ == '__main__':
    TwibotWriter().tweet(" ".join(sys.argv[1:]))
