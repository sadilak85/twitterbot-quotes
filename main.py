import tweepy
import time
import demjson
import gather_info
import random
import requests
import os
#import schedule 
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
	
	# What the bot will tweet
	filename = open('quotes.js','r') 
	tweetlist = filename.read() 
	filename.close()

	tweetlist = demjson.decode(tweetlist)

	with open('pic_urls.txt', 'r') as file:
		url_list = file.readlines()
	
	i = random.randint(0,len(url_list)-1)
	url = url_list[i]

	lang_woeid = {'en': {'NewYork': '2459115', 'LosAngeles': '2442047', 'Toronto': '4118', 'Sydney': '1105779', 'London': '44418', 'Chicago': '2379574'},
	'de': {'Germany': '23424829', 'Berlin': '638243', 'Munich': '676757', 'Hamburg': '656958'},
	'fr': {'France': '23424819', 'Paris': '615702'},
	'it': {'Italy': '23424853', 'Roma': '721943'},
	'es': {'Spain': '23424950', 'Barcelona': '753692', 'Madrid': '766273'},
	'hi': {'India': '23424848', 'Mumbai': '2295411', 'Delhi': '2295019'},
	'ar': {'SaudiArabia': '23424938', 'AbuDhabi': '1940330'},
	'tr': {'Turkey': '23424969', 'Istanbul': '2344116', 'Ankara': '2343732', 'Izmir': '2344117'},
	'ja': {'Japan': '23424856', 'Tokyo': '1118370', 'Yokohama': '1118550', 'Osaka': '15015370'},
	'nl': {'Netherlands': '23424909', 'Amsterdam': '727232', 'DenHaag': '726874', 'Rotterdam': '733075'},
	'el': {'Greece': '23424833'},
	'ko': {'Korea': '23424868', 'Seoul': '1132599', 'Busan': '1132447'},
	'no': {'Norway': '23424910'},
	'pl': {'Poland': '23424923'},
	'pt': {'Portugal': '23424925'},
	'ru': {'Russia': '23424936', 'Moscow': '2122265', 'SaintPetersburg': '2123260'},
	'sv': {'Sweden': '23424954', 'Stockholm': '906057'},
	'th': {'Thailand': '23424960'},
	'vi': {'Vietnam': '23424984'}
	}

	
	src_lang = 'en'
	dest_lang = random.choice(list(lang_woeid.keys()))
	print(dest_lang)

	#trend topic
	def trend_topic ():
		woeid = random.choice(list(lang_woeid[dest_lang].values()))
		temp = api.trends_place(woeid)
		result = [x['name'] for x in temp[0]['trends'] if x['name'].startswith('#')]
		return result

	trends_list = trend_topic ()
	while trends_list == []:
		trends_list = trend_topic ()

	print(trends_list)
	i = random.randint(0,len(tweetlist)-1)
	#j = random.randint(0,len(trends_list)-1)
	topTrend_text = str(trends_list[0])
	print(topTrend_text)
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
				translated_text = translator.translate(str(tweetlist[i]["text"]), src=src_lang, dest=dest_lang)
				print(translated_text.origin)
				print(translated_text.text)
				tweettext = translated_text.text+' -'+str(tweetlist[i]["author"])+' '+topTrend_text
			except:
				print(tweetlist[i]["text"])
				tweettext = str(tweetlist[i]["text"])+' -'+str(tweetlist[i]["author"])+' '+topTrend_text
	
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

	#search = "simulation" 
	search = topTrend_text[1:]
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
	# run the function main() every 30 minutes  
	#schedule.every(30).minutes.do(main)  

	while True:
		main()
		time.sleep(900)
		#schedule.run_pending()
#
#
#
	