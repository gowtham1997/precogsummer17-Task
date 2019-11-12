from pymongo import MongoClient
from twython import TwythonStreamer
import json

APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

connection = MongoClient()
db = connection['twitterData']

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')
            if db.tweets.count({'_id': data['id_str'] }) < 1:
	            tweetRecord = data
	            tweetRecord['_id'] = data['id_str']
	            tweetsMongo = db['tweets']
	            tweetsMongo.insert(tweetRecord)
	            if tweetsMongo.count()>=10199:
	            	self.disconnect()


    def on_error(self, status_code, data):
        print status_code
        self.disconnect()



stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track='#trump,#clinton,#USelections')
