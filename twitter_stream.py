import tweepy
import webbrowser
import json
from sys import argv


def connect():
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

    return auth


def listen(func, auth):

    class EmotionListener(tweepy.StreamListener):

        def on_status(self, status):
            func(status)

    api = tweepy.API(auth)

    listener = EmotionListener()
    myStream = tweepy.Stream(auth=api.auth, listener=listener)

    myStream.filter(languages=['en'], locations=[-115, 25, -65, 50])


def collect_sample_data(auth, number):

    class Collector(tweepy.StreamListener):

        def __init__(self, api=None, max=100):
            super(Collector, self).__init__(api=api)

            self.tweets = []
            self.max_tweets = max

        def on_status(self, status):
            self.tweets.append(status.text)

            if len(self.tweets) >= self.max_tweets:
                with open('sample_data.json', 'w') as f:
                    json.dump(self.tweets, f)
                f.close()
                return False

    api = tweepy.API(auth)

    my_stream = tweepy.Stream(auth=api.auth, listener=Collector(max=number))
    my_stream.filter(languages=['en'], locations=[-115, 25, -65, 50])


if __name__ == '__main__':

    if len(argv) != 2 or argv[1] not in ['sample', 'stream']:
        print('Please provide an argument.\nEither "sample" or "stream".')

    else:


        # authentication
        auth = connect()

        if argv[1] == 'sample':
            correct = False
            while not correct:
                number = raw_input('How many tweets should I collect? ')
                try:
                    number = int(number)
                    correct = True
                except ValueError:
                    print('Not a number!')

            collect_sample_data(auth, number)
            print('%i tweets collected into file "sample_data.json"' % number)

        elif argv[1] == 'stream':
            def tweet_printer(status):
                print(status.text)

            listen(tweet_printer, auth)
