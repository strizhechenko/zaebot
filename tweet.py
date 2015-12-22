# coding: utf-8
import os
import sys
from tweepy import OAuthHandler, API, TweepError


class Twibot():

    @staticmethod
    def conf_dict_from_env():
        app = {
            'consumer_key': os.environ.get('consumer_key'),
            'consumer_secret': os.environ.get('consumer_secret'),
        }
        user = {
            'access_token': os.environ.get('user_access_token'),
            'access_secret': os.environ.get('user_access_secret'),
        }
        for d in (app, user,):
            if None in d.values():
                raise ValueError('bad config %s' % d)
        return app, user

    @staticmethod
    def conf_dict_to_api(app, user):
        auth = OAuthHandler(app['consumer_key'], app['consumer_secret'])
        auth.set_access_token(user['access_token'], user['access_secret'])
        return API(auth)

    def __init__(self):
        app, user = self.conf_dict_from_env()
        self.api = self.conf_dict_to_api(app, user)


    def fetch(self, count=3):
        return self.api.home_timeline(count=count)


    def tweet(self, tweet):
        # 260 because encode('utf-8')
        if len(tweet) <= 260 and len(tweet) > 0:
            try:
                self.api.update_status(tweet)
                return True
            except TweepError as err:
                print tweet, err
            except Exception as err:
                print "cant log exception"
                pass
        return False

    def wipe(self):
        new_tweets = 30
        for tweet in self.fetch(200)[new_tweets:]:
            if tweet.favorite_count == 0 and tweet.retweet_count == 0:
                tweet.destroy()


if __name__ == '__main__':
    Twibot().tweet(" ".join(sys.argv[1:]))
