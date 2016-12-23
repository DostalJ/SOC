import praw
from textblob import TextBlob
from time import sleep
import keys

reddit = praw.Reddit(client_id=keys.client_id,
                     client_secret=keys.client_secret,
                     password=keys.password,
                     username=keys.username,
                     user_agent=keys.user_agent)

keywords = ['islam', 'isis', 'islamic state', 'muslim', 'muslims', 'terrorist', 'refugee', 'refugees']


subreddit = reddit.subreddit('news')

for i in range(12):
    sentiment = 0
    num_of_comments = 0

    for comment in subreddit.comments():
        if any(word in comment.body.lower() for word in keywords):
            num_of_comments += 1
            sentiment = (sentiment + TextBlob(comment.body.lower()).sentiment.polarity)/2
    print('Step:', i)
    print('Comments:', num_of_comments)
    print('Sentiment: {:.5f}'.format(sentiment))
    print('-'*40)
    sleep(30*60)
