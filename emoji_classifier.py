from csv import DictReader
from pandas import read_csv
from numpy import mean

class EmojiClassifier():

    def __init__(self):
        def load_dictionary():
            """Load and transform the provided Emoji Sentiment data."""
            df = read_csv('datasources/Emoji_Sentiment_Data_v1.0.csv')
            df['Sum'] = df['Positive'] + df['Neutral'] + df['Negative']
            df['Score'] = ((9 * df['Positive'] + 5 * df['Neutral'] +
                           df['Negative']) / df['Sum'])
            df['Variance'] = ((81 * df['Positive'] + 25 * df['Neutral'] +
                              df['Negative']) / df['Sum'] - df['Score'] ** 2)

            # center data around 5.06
            df['Score'] = df['Score'] - (df['Score'].mean() - 5.09)

            # create a dict to lookup mean and variance for a given emoji
            data = {}
            for index, row in df.iterrows():
                data[row['Emoji'].decode('utf-8')] = {
                    'mean': row['Score'],
                    'variance': row['Variance']
                }
            return data

        self.emoji_dict = load_dictionary()

    def classify(self, emoji_list):
        scores = [self.emoji_dict[emoji]['mean'] for emoji in emoji_list
                  if emoji in self.emoji_dict]
        return mean(scores)
