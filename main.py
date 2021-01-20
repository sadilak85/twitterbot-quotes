import tweepy
import time
import demjson
import gather_info

def main():
	with open('API_keys.txt', 'r') as file :
		consumer_key = file.readline().strip()
		consumer_secret = file.readline().strip()
		access_token = file.readline().strip()
		access_token_secret = file.readline().strip()
	
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	user = api.me()
	
	gather_info.displayinfo(user)
	
	# What the bot will tweet
	filename = open('quotes.js','r') 
	tweetlist = filename.read() 
	filename.close()

	tweetlist = demjson.decode(tweetlist)

	try:
		for elt in tweetlist: 
			api.update_status(elt["text"]+' -'+elt["author"])
			time.sleep(3600) 

	except tweepy.error.TweepError:
		pass
		
	search = "simulation"
	numberOfTweets = 2

	def limit_handle(cursor):
		while True:
			try:
				yield cursor.next()
			except tweepy.RateLimitError:
				time.sleep(1000)

	#Be nice to your followers. Follow everyone!
	#for follower in limit_handle(tweepy.Cursor(api.followers).items()):
	#  if follower.name == 'Usernamehere':
	#    print(follower.name)
	#    follower.follow()


	# Be a narcisist and love your own tweets. or retweet anything with a keyword!
	for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
		try:
			tweet.favorite()
			print('Retweeted the tweet')
		except tweepy.TweepError as e:
			print(e.reason)
		except StopIteration:
			break

if __name__ == "__main__":
    main()
	
	