import praw
from textblob import TextBlob
import keys

reddit = praw.Reddit(client_id=keys.client_id,
                     client_secret=keys.client_secret,
                     password=keys.password,
                     username=keys.username,
                     user_agent=keys.user_agent)

subreddit = reddit.subreddit('news')

for comment in subreddit.comments():
    print(comment.body)
    print(TextBlob(comment.body).sentiment)
    print('-'*80)
