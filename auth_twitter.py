import tweepy, webbrowser, os

CONSUMER_KEY = os.environ.get(CONSUMER_KEY)
CONSUMER_SECRET = os.environ.get(CONSUMER_SECRET)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth_url = auth.get_authorization_url()
webbrowser.open(auth_url)
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
print auth.access_token
print auth.access_token_secret
