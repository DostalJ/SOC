import basc_py4chan
from textblob import TextBlob
from time import sleep


keywords = ['islam', 'isis', 'islamic state', 'muslim', 'terrorist', 'refugee', 'refugees']

for i in range(10):
    sentiment = 0
    num_of_threads = 0

    board = basc_py4chan.Board('news')
    all_threads = board.get_all_threads()
    for thread in all_threads:
        if any(word in thread.topic.subject for word in keywords) or any(word in thread.topic.text_comment for word in keywords):
            sentiment = (sentiment + TextBlob(thread.topic.subject + thread.topic.text_comment).sentiment.polarity)/2
            num_of_threads += 1
            for post in thread.posts:
                sentiment = (sentiment + TextBlob(post.text_comment).sentiment.polarity)/2
    print('Sentiment at step {}: {:.5f}'.format(i, sentiment))    
    sleep(60)
