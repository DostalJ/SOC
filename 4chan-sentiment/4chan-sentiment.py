import basc_py4chan
from textblob import TextBlob
from time import sleep


keywords = ['islam', 'isis', 'islamic state', 'muslim', 'muslims', 'terrorist', 'refugee', 'refugees']

for i in range(12):
    sentiment = 0
    num_of_threads = 0

    board = basc_py4chan.Board('news')
    all_threads = board.get_all_threads()
    for thread in all_threads:
        if any(word in thread.topic.text_comment.lower() for word in keywords):
            sentiment = (sentiment + TextBlob(thread.topic.text_comment.lower()).sentiment.polarity)/2
            num_of_threads += 1
            for post in thread.posts:
                sentiment = (sentiment + TextBlob(post.text_comment.lower()).sentiment.polarity)/2
    print('Step:', i)
    print('Threads:', num_of_threads)
    print('Sentiment: {:.5f}'.format(sentiment))
    print('-'*40)
    sleep(30*60)
