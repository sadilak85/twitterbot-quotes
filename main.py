import tweepy
import time
import demjson
import gather_info
import random
import requests
import os
import schedule 
from googletrans import Translator 

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
	
	temp = api.trends_place(2344116) #WOEID of Turkey: 23424969   Istanbul: 2344116 
	trends_list = [x['name'] for x in temp[0]['trends'] if x['name'].startswith('#')]
	print(trends_list)


	# What the bot will tweet
	filename = open('quotes.js','r') 
	tweetlist = filename.read() 
	filename.close()

	tweetlist = demjson.decode(tweetlist)

	with open('pic_urls.txt', 'r') as file:
		url_list = file.readlines()
	
	i = random.randint(0,len(url_list)-1)
	url = url_list[i]

	i = random.randint(0,len(tweetlist)-1)
	j = random.randint(0,len(trends_list)-1)
	translator = Translator()
	try: 
		#api.update_status(tweetlist[i]["text"]+' -'+tweetlist[i]["author"])
		filename = 'temp.jpg'
		request = requests.get(url, stream=True)
		if request.status_code == 200:
			with open(filename, 'wb') as image:
				for chunk in request:
					image.write(chunk)
			

			try:
				translated_text = translator.translate(str(tweetlist[i]["text"]), src='en', dest='tr')
				print(translated_text.origin)
				print(translated_text.text)
				tweettext = translated_text.text+' -'+str(tweetlist[i]["author"])+' '+str(trends_list[j])
			except:
				print(tweetlist[i]["text"])
				tweettext = str(tweetlist[i]["text"])+' -'+str(tweetlist[i]["author"])+' '+str(trends_list[j])
				
			api.update_with_media(filename, status=tweettext)
			os.remove(filename)
		else:
			print("Unable to download image")
	
	except tweepy.error.TweepError:
		pass



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

	search = "simulation"
	numberOfTweets = 10

	# Be a narcisist and love your own tweets. or retweet anything with a keyword!
	for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
		try:
			tweet.favorite()
			print('Retweeted the tweet')
		except tweepy.TweepError as e:
			print(e.reason)
		except StopIteration:
			break
			
	search = "valentines quotes"
	numberOfTweets = 10

	# Be a narcisist and love your own tweets. or retweet anything with a keyword!
	for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
		try:
			tweet.favorite()
			print('Retweeted the tweet')
		except tweepy.TweepError as e:
			print(e.reason)
		except StopIteration:
			break

			
	search = "scientific quotes"
	numberOfTweets = 10

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
	# run the function main() every 30 minutes  
	schedule.every(60).minutes.do(main)  

	while True:
		schedule.run_pending()
		time.sleep(1000)


	
	