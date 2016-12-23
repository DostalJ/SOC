from tweepy import StreamListener
import json, time, sys

# http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/


class SListener(StreamListener):

    def __init__(self, api = None, fprefix = 'stream'):
        self.api = api or API()
        self.counter = 0
        self.fprefix = fprefix
        self.output = open(fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json',
                           'w')
        self.delout = open('delete.txt', 'a') # for appendind to the end of the file

    def on_data(self, data):
        if 'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print(warning['message'])
            return False

    def on_status(self, status):
        # print(self.counter)
        self.output.write(json.loads(status)['text'])
        self.output.write(status)#, + '\n')
        self.counter += 1

        if self.counter >= 20000:
            self.output.close()
            self.output = open(self.prefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json',
                               'w')
            self.counter = 0
        return

    def on_delete(self, status_id, uder_id):
        self.delout.write(str(status_id) + '\n')
        return

    def on_limit(self, track):
        sys.stderr.write(track, '\n')
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + '\n')
        return False

    def on_timeout(self):
        sys.stderr.write('Timeout, sleeping for 60 seconds...\n')
        time.sleep(60)
        return
