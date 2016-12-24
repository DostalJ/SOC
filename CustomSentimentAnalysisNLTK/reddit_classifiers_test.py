import praw
from textblob import TextBlob
from time import sleep
import keys

"""
Trying different classifiers
"""


reddit = praw.Reddit(client_id=keys.client_id,
                     client_secret=keys.client_secret,
                     password=keys.password,
                     username=keys.username,
                     user_agent=keys.user_agent)

keywords = ['islam', 'isis', 'islamic state', 'muslim', 'muslims', 'terrorist', 'refugee', 'refugees']

subreddit = reddit.subreddit('news')

from sentiment_classifier import Classify
RC = Classify('short_reviews')
TC = Classify('twitter')
for comment in subreddit.comments():
    if any(word in comment.body.lower() for word in keywords):
        sentTB = TextBlob(comment.body.lower()).sentiment.polarity
        print('Comment:', comment.body)
        print('TextBlob: {:.5f}'.format(sentTB))
        print('Movie Reviews:', RC.sentiment(comment.body))
        print('Twitter:', TC.sentiment(comment.body))
        print('-'*40)
