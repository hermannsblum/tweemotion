import tweepy
import webbrowser
import json
from sys import argv
from pprint import pprint


def connect(remote=False):
    token = 'H38UfwBmX3AesWlUXMDmCRkXV'
    secret = 'Ml7DJ5LmWjsogw8cMoyqC0FX2JtLwY6I9FFdOOIUBymj0E8PGF'

    auth = tweepy.OAuthHandler(token, secret)

    # get requet token
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    # login
    if remote:
        print('open the following url in your browser: %s' % redirect_url)
    else:
        print('logging you in to twitter...')
        webbrowser.open(redirect_url, new=2)

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


def collect_sample_data(auth, number, geo=False):

    class Collector(tweepy.StreamListener):

        def __init__(self, api=None, max=100):
            super(Collector, self).__init__(api=api)

            self.tweets = []
            self.max_tweets = max

        def on_status(self, status):
            if geo:
                # add information about geolocation in lon-lat-format
                if status.geo is not None:
                    # we have detailed coordinate information
                    coordinates = (status.geo['coordinates'][1],
                                   status.geo['coordinates'][0])
                    data = {'text': status.text,
                            'coordinates': coordinates}
                elif status.place is not None:
                    # we have information about the city
                    bottom_left = status.place.bounding_box.origin()
                    upper_right = status.place.bounding_box.corner()
                    # find center of city
                    center = ((bottom_left[0] + upper_right[0]) / 1.0,
                              (bottom_left[1] + upper_right[1]) / 1.0)
                    data = {'text': status.text,
                            'coordinates': center}
                else:
                    # we can't use this tweet
                    return True
            else:
                data = status.text
            self.tweets.append(data)

            if len(self.tweets) >= self.max_tweets:
                with open('sample_data.json', 'w') as f:
                    json.dump(self.tweets, f)
                f.close()
                print('%i tweets collected into file "sample_data.json"'
                      % len(self.tweets))
                return False

    api = tweepy.API(auth)

    my_stream = tweepy.Stream(auth=api.auth, listener=Collector(max=number))
    my_stream.filter(languages=['en'], locations=[-115, 25, -65, 50])


if __name__ == '__main__':

    if len(argv) != 2 or argv[1] not in ['sample', 'stream']:
        print('Please provide an argument.\nEither "sample" or "stream".')

    else:
        remote = " "
        while remote not in ['y', 'n']:
            remote = raw_input('are you working remotely? (y/n) ')

        # authentication
        auth = connect(remote=(remote == 'y'))

        if argv[1] == 'sample':
            correct = False
            while not correct:
                number = raw_input('How many tweets should I collect? ')
                try:
                    number = int(number)
                    correct = True
                except ValueError:
                    print('Not a number!')
            geo = " "
            while geo not in ['y', 'n']:
                geo = raw_input('Collect coordinates? [y/n] ')

            collect_sample_data(auth, number, geo=(geo == 'y'))

        elif argv[1] == 'stream':
            def tweet_printer(status):
                print(status.text)

            listen(tweet_printer, auth)
