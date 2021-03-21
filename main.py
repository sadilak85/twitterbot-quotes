import tweepy
import time
import demjson
import gather_info
import random
import requests
import os
import re
#import schedule 
from google_trans_new import google_translator 

import delete_tweets
 

tmp_url_list = []
_tmptrendlist= []

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
	
	# delete older tweets first:
	delete_tweets.delete_tweets_func(api)
	
	# What the bot will tweet
	filename = open('quotes.js','r') 
	tweetlist1 = filename.read() 
	filename.close()
	
	filename = open('quotes2.json','r',encoding='utf-8') 
	tweetlist2 = filename.read() 
	filename.close()

	filename = open('quotes3.json','r',encoding='utf-8') 
	tweetlist3 = filename.read() 
	filename.close()

	tweetlist1 = demjson.decode(tweetlist1) #js 
	tweetlist2 = demjson.decode(tweetlist2) #json
	tweetlist3 = demjson.decode(tweetlist3) #json
	tweetlist = tweetlist1 + tweetlist2 + tweetlist3

	with open('pic_urls.txt', 'r') as file:
		url_list = file.readlines()
		
	i = random.randint(0,len(url_list)-1)
	if tmp_url_list != []:
		for value in tmp_url_list:
			if url_list[i] == value:
				pass
			else:
				url = url_list[i]
				tmp_url_list.append(url)
	else:
		url = url_list[i]
		tmp_url_list.append(url)

	lang_woeid = {#'en': {'NewYork': '2459115', 'LosAngeles': '2442047', 'Toronto': '4118', 'Sydney': '1105779', 'London': '44418', 'Chicago': '2379574'},
	#'de': {'Germany': '23424829', 'Berlin': '638243', 'Munich': '676757', 'Hamburg': '656958'},
	#'fr': {'France': '23424819', 'Paris': '615702'},
	#'it': {'Italy': '23424853', 'Roma': '721943'},
	#'es': {'Spain': '23424950', 'Barcelona': '753692', 'Madrid': '766273'},
	#'hi': {'India': '23424848', 'Mumbai': '2295411', 'Delhi': '2295019'},
	#'ar': {'SaudiArabia': '23424938', 'AbuDhabi': '1940330'},
	'tr': {'Turkey': '23424969', 'Istanbul': '2344116', 'Ankara': '2343732', 'Izmir': '2344117'},
	#'ja': {'Japan': '23424856', 'Tokyo': '1118370', 'Yokohama': '1118550', 'Osaka': '15015370'},
	#'nl': {'Netherlands': '23424909', 'Amsterdam': '727232', 'DenHaag': '726874', 'Rotterdam': '733075'},
	#'ko': {'Korea': '23424868', 'Seoul': '1132599', 'Busan': '1132447'},
	#'ru': {'Russia': '23424936', 'Moscow': '2122265', 'SaintPetersburg': '2123260'},
	#'sv': {'Sweden': '23424954', 'Stockholm': '906057'},
	#'th': {'Thailand': '23424960'},
	#'vi': {'Vietnam': '23424984'}
	}

	
	src_lang = 'en'
	dest_lang = random.choice(list(lang_woeid.keys()))
	print(dest_lang)

	#trend topic
	def trend_topic ():
		woeid = random.choice(list(lang_woeid[dest_lang].values()))
		try:
			temp = api.trends_place(woeid)
			result = [x['name'] for x in temp[0]['trends'] if x['name'].startswith('#')]
		except:
			result = []
		return result

	trends_list = trend_topic ()
	while trends_list == []:
		trends_list = trend_topic ()

	print(trends_list)
	
	
	topTrend_text = str(trends_list[0])
	while topTrend_text in _tmptrendlist:
		j = random.randint(0,len(trends_list)-1)
		topTrend_text = str(trends_list[j])
	
	_tmptrendlist.append(topTrend_text)	
	
	print(topTrend_text)
	#translator = Translator()
	translator = google_translator() 


	# for i in range(len(tweetlist)):
	# 	translated_ = translator.translate(str(tweetlist[i]["text"]), lang_tgt='tr')
	# 	tweetlist[i]['text'] = translated_

	#list_topTrend_words = re.findall('([A-Z][a-z]+)', topTrend_text[1:], re.UNICODE)
	list_topTrend_words=[]
	keywords =[]
	pos = [i for i,e in enumerate(topTrend_text[1:]+'A') if e.isupper()]
	for j in range(len(pos)-1):
		_tmp = topTrend_text[1:][pos[j]:pos[j+1]]
		if len(_tmp)>1:
			list_topTrend_words.append(_tmp)

	for trendWord in list_topTrend_words:
		print (trendWord)
		keyword = translator.translate(trendWord, lang_tgt='en').strip()
		print (keyword)
		keywords = list(filter(lambda twittext: keyword in twittext['text'],  tweetlist  ))

	if keywords != []:
		print(keywords)
		tweetlist = keywords

	tweetlistitem = random.randint(0,len(tweetlist)-1) # RANDOM ITEM IN LIST
	try: 
		#api.update_status(tweetlist[i]["text"]+' -'+tweetlist[i]["author"])
		filename = 'temp.jpg'
		request = requests.get(url, stream=True)
		if request.status_code == 200:
			with open(filename, 'wb') as image:
				for chunk in request:
					image.write(chunk)
			try:
				translated_text = translator.translate(str(tweetlist[tweetlistitem]["text"]), lang_tgt='tr')
				print(translated_text)
				tweettext = translated_text+' -'+str(tweetlist[tweetlistitem]["author"])+' '+topTrend_text
			except:
				print(tweetlist[tweetlistitem]["text"])
				tweettext = str(tweetlist[tweetlistitem]["text"])+' -'+str(tweetlist[tweetlistitem]["author"])+' '+topTrend_text
	
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
			
def check_positive_integer(num):
	try:
		val = int(num)
		if val <= 0:  # if not a positive int print message and ask for input again
			print("Sorry, input must be a positive integer and not zero, try again")
			return False
		return True
	except ValueError:
		print("That's not an integer!")
		return False

if __name__ == "__main__":
	# run the function main() every 30 minutes  
	#schedule.every(30).minutes.do(main)
	
	while True:
		_time = input("Give repeat time in sec:\n")
		if check_positive_integer(_time):
			break
	
	while True:
		main()
		time.sleep(int(_time))
		#schedule.run_pending()
#
#
#
	