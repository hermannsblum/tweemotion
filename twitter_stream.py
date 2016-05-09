import tweepy
import webbrowser

token = 'H38UfwBmX3AesWlUXMDmCRkXV'
secret = 'Ml7DJ5LmWjsogw8cMoyqC0FX2JtLwY6I9FFdOOIUBymj0E8PGF'

auth = tweepy.OAuthHandler(token, secret)

# get requet token
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')

# login
print('logging you in to twitter...')
webbrowser.open(redirect_url, new=2)
#
verifier = raw_input('Verifier:')

try:
    auth.get_access_token(verifier)
except tweepy.TweepError:
    print 'Error! Failed to get access token.'


class EmotionListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

api = tweepy.API(auth)

listener = EmotionListener()
myStream = tweepy.Stream(auth=api.auth, listener=listener)

myStream.filter(languages=['en'], locations=[-115, 25, -65, 50])
