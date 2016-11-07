# PreCog Summer Task A- US Elections textual analysis with twitter

The app is built in Flask.All subtasks are  carried out in the backend(Querying the database) and data is sent to frontend as a json upon a AJAX request.The data is later visualised using charts plotted using [chartist.js](https://gionkunz.github.io/chartist-js/).Below is the set of subtasks with description of how I attempted to solve them,their drawbacks and scope for improvement. 

*	Collection of tweets:
		The tweets are collected using Twython and the Twitter Streaming APIs[^1].
		[^1]:If streaming responds with a 404 error,change system time and date to GMT timezone or update system time using ntp package.
		Refrences used:[PSOSM](https://www.youtube.com/watch?v=lIVbvzwIgzw PSOSM NPTEL Videos),[Twitter Streaming API documentation](https://dev.twitter.com/streaming/overview)

*	Location of Tweets:
		*	The Location of the user is taken from coordinates field in tweet object amd plotted using 
			[leaflat.js](http://leafletjs.com/).The coordiantes are stored in a [geoJSON](http://geojson.org/) format and sent to leaflat to mark them on the map.
			Since,most of the users do not enable geo location,the results would not be useful for analysis.
	
		*	An approximate location can be obtained by converting textual user's location(location specified at 	time of account creation) to coordinates using geocoding libraries like [geocoder](http://geocoder.readthedocs.io/) and plotting the results with leaflat.
			Even though this method produced good results ,it was **slow** and this failed to recognise imaginary user locations like 'Heaven','Hell','Somewhere I Belong',etc.

		Refrences used:[Geolocation](https://marcobonzanini.com/2015/06/16/mining-twitter-data-with-python-and-js-part-7-geolocation-and-interactive-maps/)

*	List of Top 10 Hashtags being used in the stream:

		Hashtags of a tweet can be accessed under `tweet['entities']['hashtags']` or with a regex pattern match.Each hashtag is encoded in *UTF-8* and converted to lowercase[^2] and stored in a python dictionary which also stores its frequency.This is later converted to a list of tuples and sorted in decreasing order of frequency to get top 10 tweets.
		[^2]:The Hashtags are converted to lower case to avoid redundant hashtags(#Trump and #trump,etc).

*	Distribution of Original Tweets vs Retweeted Tweets:
	
		Retweets are found by searching for the word *RT* or an *ellipsis* “…” in the tweet.
		Their distribution vs original tweets is then plotted using [chartist.js](https://gionkunz.github.io/chartist-js/).

*	Distribution of favorite counts on Original Tweets:
		
		Since the tweets are streamed live ,Newly created tweets have their expected zero favorites count.
		An alternate approach can be adopted by finding the present favorite count of the tweet by searching by its *id* using Twitter rest API.But this method cannot be performed dynamically on the backend as it slows the application.

*	Distribution of Type of Tweet i.e. Text, Image, Text+Image:
		
		A tweet's text is assumed to be what's left after removing mentions,urls and hashtags from a tweet.Using [urlparse](https://docs.python.org/2/library/urlparse.html) urls are identified.Similarly,mentions and hashtags are identified.The length of remaining text is calculated to find out whether tweet contains text.Images are checked by finding the length of media field under entities - 'len(tweet['entities'].get('media', [])) >0'.

		Refrences used:[stackoverflow](http://stackoverflow.com/questions/8376691/how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression)

*	Who is more popular, Hillary or Trump?:
		
		The popularity is assumed to be sum of number of *Unique user tweets*,*Retweets* in popular hashtags -#trump,#maga,#draintheswamp,#trumppence2016,#clinton,#hillary,#imwithher,#strongertogether and *number of tweets with mentions* - @realDonaldTrump,@HillaryClinton
		
		A tweet with hashtags like '#trump','#clinton',etc can be used to support,criticize and make rude or sarcastic statements.A better analysis can be obtained by counting number of positive and negative words to get a sense of tweet(whether positive or negative) with respect to the tweet also taking sarcasm and not jokes into account.This can help predict popularity with more accuracy.

