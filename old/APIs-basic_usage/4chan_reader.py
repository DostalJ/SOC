import basc_py4chan
# http://basc-py4chan.readthedocs.io/en/latest/index.html

board = basc_py4chan.Board('r')
thread_ids = board.get_all_thread_ids()
thread = board.get_thread(thread_id=thread_ids[5])
for post in thread.posts:
    print(post.text_comment)
    print('-'*60)
