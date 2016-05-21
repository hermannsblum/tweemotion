import tweepy
import webbrowser
import json
from sys import argv
import redis
from emoji_classifier import EmojiClassifier
from tweet_cleanup import cleanup
from compSent import compSent
from numpy import isnan

red = redis.StrictRedis()


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


def get_coordinates(tweet):
    """Get coordinates of tweet in lat-lon-format."""
    if tweet.geo is not None:
        # we have detailed coordinate information
        coordinates = (tweet.geo['coordinates'][1],
                       tweet.geo['coordinates'][0])
    elif tweet.place is not None:
        # we have information about the city
        bottom_left = tweet.place.bounding_box.origin()
        upper_right = tweet.place.bounding_box.corner()
        # find center of city
        coordinates = ((bottom_left[0] + upper_right[0]) / 2.0,
                       (bottom_left[1] + upper_right[1]) / 2.0)
    else:
        # we can't use this tweet
        return None
    return coordinates


def get_sentiment(tweet, emoji_classifier, text_classifier):
    tweet, emojis = cleanup(tweet.text)

    emoji_sentiment = emoji_classifier.classify(emojis)
    text_sentiment = text_classifier.compSentiment_v(tweet)

    if not isnan(emoji_sentiment):
        return 0.65 * emoji_sentiment + 0.35 * text_sentiment
    else:
        return text_sentiment


def get_emotion(tweet, text_classifier):
    text, _ = cleanup(tweet.text)
    valence = text_classifier.compSentiment_v(text)
    arousal = text_classifier.compSentiment_a(text)
    dominance = text_classifier.compSentiment_d(text)

    if isnan(valence) or isnan(arousal) or isnan(dominance):
        return None
    if valence >= 5 and arousal >= 5 and dominance >= 5:
        return 'happy'
    elif valence >= 5 and arousal >= 5 and dominance < 5:
        return 'excited'
    elif valence >= 5 and arousal < 5 and dominance >= 5:
        return 'relaxed'
    elif valence >= 5 and arousal < 5 and dominance < 5:
        return 'satisfied'
    elif valence < 5 and arousal >= 5 and dominance >= 5:
        return 'angry'
    elif valence < 5 and arousal >= 5 and dominance < 5:
        return 'frightened'
    elif valence < 5 and arousal < 5 and dominance >= 5:
        return 'bored'
    elif valence < 5 and arousal < 5 and dominance < 5:
        return 'sad'
    return None


def collect_sample_data(auth, number, geo=False):

    class Collector(tweepy.StreamListener):

        def __init__(self, api=None, max=100):
            super(Collector, self).__init__(api=api)

            self.tweets = []
            self.max_tweets = max

        def on_status(self, status):
            if geo:
                # add information about geolocation in lon-lat-format
                coord = get_coordinates(status)
                if coord is not None:
                    data = {'text': status.text,
                            'coordinates': coord}
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
    # my_steam.filter(track=['#MySpecialHashtag', '#AlsoThisHashtag'])



if __name__ == '__main__':

    if len(argv) != 2 or argv[1] not in ['sample', 'stream', 'publish']:
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

        elif argv[1] == 'publish':
            emoji_sentiment = EmojiClassifier()
            text_sentiment = compSent()

            def tweet_publisher(status):
                sentiment = get_sentiment(status, emoji_sentiment,
                                          text_sentiment)
                emotion = get_emotion(status, text_sentiment)

                # try to get the state
                place_name = status.place.full_name.split(', ')
                if not len(place_name) > 1:
                    return
                state_list = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT',
                              'DC', 'DE', 'FL', 'FM', 'GA', 'GU', 'HI', 'IA',
                              'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD',
                              'ME', 'MH', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT',
                              'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY',
                              'OH', 'OK', 'OR', 'PA', 'PR', 'PW', 'RI', 'SC',
                              'SD', 'TN', 'TX', 'UM', 'UT', 'VA', 'VI', 'VT',
                              'WA', 'WI', 'WV', 'WY']
                state = place_name[1]
                if state not in state_list:
                    return
                # only use the tweet if we got a sentiment
                if not isnan(sentiment) and emotion is not None:
                    data = {
                        'tweet': status.text,
                        'coordinates': get_coordinates(status),
                        'sentiment': sentiment,
                        'emotion': emotion,
                        'state': state
                    }
                    red.publish('tweet_stream', json.dumps(data))

            listen(tweet_publisher, auth)

        elif argv[1] == 'stream':
            def tweet_printer(status):
                print(status.text)

            listen(tweet_printer, auth)
