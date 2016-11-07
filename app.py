import string
import urlparse
# import geocoder
from flask import Flask, render_template, jsonify
from random import sample
from flask_pymongo import PyMongo
 
app=Flask(__name__)
 
#: connecting to the database
app.config['MONGO_DBNAME'] = 'twitterData'
app.config['MONGO_URI'] = 'mongodb://gowtham:password1@ds143767.mlab.com:43767/twitterdata'
 
mongo = PyMongo(app)
 
@app.route('/')
def index():
    return render_template("chart.html")
 
'''
    data route sends calculated json data to frontend upon an
    AJAX request
'''
 
@app.route('/data')
def data():
 
    tweets_collection = mongo.db.tweets
    tweets=tweets_collection.find()
 
    '''
        text_counter - Number of tweets that only contain text
        image_counter - Number of tweets that only contain image
        text_and_image_counter - Number of tweets that contain both
    '''
    text_counter=0
    image_counter=0
    text_and_image_counter=0
 
    '''
        hashtag_frequency is a dictionary to store frequency of hashtags
    '''
 
    hashtag_frequency={}
 
    '''
         retweets - Number of retweets
    '''
 
    retweets = 0
 
    '''
        geopoints is a array of geopoint(geoJSON storing
        coordinate(longitude,latitude) and type(point,region,etc))
    '''
 
    geopoints=[]
 
    '''
        trump_popularity - sum of unique user tweets, number of retweets of users using hashtags stored in
                            trump_hashtags
        hillary_popularity- sum of unique user tweets, number of retweets of users using hashtags stored in
                            hillary_hashtags
        trump_set          - set which stores unique user ids of tweets with trump_hashtags
        hillary_set          - set which stores unique user ids of tweets with trump_hashtags
        trump_mentions      - Number of '@realDonaldTrump' mentions
        hillary_mentions  - Number of '@HillaryClinton' mentions
        trump_retweets      - number of Retweets with trump_hashtags
        hillary_retweets  - number of Retweets with hillary_hashtags
        trump_hashtags      - list containing popular hashtags related to Trump
        hillary_hashtags  - list containing popular hashtags related to Trump
    '''
 
    trump_popularity=0
    hillary_popularity=0
    trump_set=set()
    hillary_set=set()
    trump_mentions=0
    hillary_mentions=0
    trump_retweets=0
    hillary_retweets=0
    trump_hashtags=['#trump','#maga','#draintheswamp','#trumppence2016']
    hillary_hashtags=['#clinton','#hillary','#imwithher','#strongertogether']
 
    for tweet in tweets:
 
        #: tweet_text,tweet_image,tweet_image_and_text - boolean flags to identify type of tweet
        tweet_text = tweet_image = tweet_image_and_text = False
 
        tweet_string = tweet['text']
 
        #: tweet_string_parsed stores tweet text without urls, hashtags and mentions
        tweet_string_parsed = ''
 
        user_id = tweet['user']['id']
 
        #: RT_status - boolean flag indicating whether tweet is a Retweet/original
        RT_status=False
        
        for tweet_word in tweet_string.split():
 
            if(tweet_word=="RT" or tweet_word=="..."):
                RT_status=True
            
            #: Checking if string is a url
            scheme, netloc, path, params, query , fragment = urlparse.urlparse(tweet_word)
 
            if scheme and netloc:
                pass
            #: checking if string is a mention
            elif tweet_word[:1] =='@':
                if tweet_word.lower()=='@realdonaldtrump':
                    trump_mentions+=1
                elif tweet_word.lower()=='@hillaryclinton':
                    hillary_mentions+=1
            #: checking if string is a hashtag
            elif tweet_word[:1] == '#':
                if tweet_word.lower() in trump_hashtags:
                    trump_set.add(user_id)
                    if RT_status == True:
                        trump_retweets+=1
                elif tweet_word.lower() in hillary_hashtags:
                    hillary_set.add(user_id)
                    if RT_status == True:
                        hillary_retweets+=1
            else:
                '''
                    tweet_string_parsed stores what's left in the tweet after removing 
                    mentions,hashtags and urls.
                ''' 
                tweet_string_parsed = tweet_string_parsed.strip() + ' ' + tweet_word

        if(len(tweet_string_parsed)>0):
            tweet_text = True
        #: To check if tweet contains an image
        if len(tweet['entities'].get('media', [])) >0:
            tweet_image = True

        if(tweet_text and tweet_image):
            text_and_image_counter += 1
        elif tweet_text:
            text_counter+=1
        else:
            image_counter+=1
        '''
            hashtag_record stores twitter's hashtag object
        '''
        for hashtag_record in tweet['entities']['hashtags']:
        #: words are encoded in utf-8 and lowercased to avoid redundant hahtags like
        #: #hillary and #Hillary
                word = hashtag_record['text'].encode('utf-8').lower()
                count=hashtag_frequency.get(word,0)
                hashtag_frequency[word]=count+1
                
        if RT_status == True:
            retweets+=1

        '''
            If user has enabled his geo location on twitter.
            Note: 'geo' field is deprecated. Ref: https://dev.twitter.com/overview/api/tweets

            Users tweets with geo enabled are very rare and streaming for geo_enabled tweets
            does'nt yield fruitful results.
        '''
        if(tweet['coordinates'] != None):
            geopoint={
                "coordinates": [],
                "type": "Point"
            }

            '''
                Approximate user location can be calculated by assuming the tweet's location to
                user's location(given at time of creation).
                
                Drawback: Some people type imaginary locations - Heaven, hell,etc and the api takes a 
                          lot of time to process all tweets
            '''
            # g = geocoder.google(tweet['user']['location'])
            # print(tweet['user']['location'])
            geopoint['coordinates']=tweet['coordinates']["coordinates"]
            geopoints.append(geopoint)
 
    '''
        tweet_type_frequency stores frequency of type of tweet(text,images and both) 
    '''
    
    tweet_type_frequency = []
    tweet_type_frequency.extend((text_counter,image_counter,text_and_image_counter))

    '''
        hashtag_list stores a list of tuples(frequency of hashtag,hashtag) 
        arranged in descending order of  frequency of hashtag.

        hashtag_string stores list of top 10 hashtags
        hashtag_count stores frequencies of top 10 hashtags

    '''
    hashtag_list=[(hashtag_frequency[key],key) for key in hashtag_frequency]
    hashtag_list.sort()
    hashtag_list.reverse()
    hashtag_string=[]
    hashtag_count=[]
    for hashtag in hashtag_list[:10]:
        hashtag_count.append(hashtag[0])
        hashtag_string.append(hashtag[1])
 
    print(len(trump_set)+trump_retweets+trump_mentions)
    print(len(hillary_set)+hillary_retweets+hillary_mentions)
 
    trump_popularity=len(trump_set)+trump_retweets+trump_mentions
    hillary_popularity=len(hillary_set)+hillary_retweets+hillary_mentions

    #: return the results in json format to frontend.
 
    return jsonify({
        'retweets_count':retweets,
        'top_trends_string':hashtag_string,
        'top_trends_count':hashtag_count,
        'tweet_type': tweet_type_frequency,
        'trump_popularity':trump_popularity,
        'hillary_popularity':hillary_popularity,
        'geodata': geopoints
                })
 
 
if __name__ == "__main__":
    app.run(debug=True)