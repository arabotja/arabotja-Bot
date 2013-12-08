#!/usr/bin/python
#-*- coding: UTF-8 -*-
 
import tweepy
import bitly_api
import sys, pickle, time, datetime
import re
from librarian import DumpTruck
 
# enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'yourConsumerKey'
CONSUMER_SECRET = 'yourConsumerSecret'
ACCESS_KEY = 'yourAccessKey'
ACCESS_SECRET = 'yourAccessSecret'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class BabyBird(DumpTruck):

	def __init__(self, name):
		DumpTruck.__init__(self, name)
		self.basket = []

	def shortenUrl(self,longurl): # bit.ly url shortener API
		API_USER = "yourUsername"
		API_KEY = "yourAPIKey"
		b = bitly_api.Connection(access_token = API_KEY)
		
		response = b.shorten(uri = longurl)
		shortUrl = response['url']

		return shortUrl

	def tweetMsg(self, e_arg): # tweepy API
		api.update_status(e_arg)
		
		try:
		 	print 'Tweet! : ' + e_arg
		
		except Exception, e:
		 	print str(e) 

	def wakeBird(self): # Turn key for first start or reboot (small DB making to prevent duplication)
		self.makeFilter('정보', 3)
		print '-' * 50 + 'makeFilter() Success'

	def feedBird(self): # Core; Scrap recent list - Filter - Refine message - Hand over bullet
		self.dumpRecent('정보', 1)
		print '-' * 50 + 'dumpRecent() Success'
		self.judgeArticle()
		print '-' * 50 + 'judgeArticle() Success'

		for i in self.basket:
			articleNumber = re.findall(r'(\d{10})', i[1])
			longurl = self.url + str(articleNumber[0])
			e_arg = i[0].encode('UTF-8') + ' ' +  self.shortenUrl(longurl).encode('UTF-8') # encode when you moving around 'unicode + int' list or etc.
			e_arg = e_arg[0:138] # Twitter allows only char 140
			self.tweetMsg(e_arg)
			time.sleep(5)
		
		else:
			print '-' * 50 + 'Nothing in buffer.'



if __name__ == '__main__':
	try:
		arabotja = BabyBird('ilbe')
		arabotja.feedBird()
		timespamp = datetime.datetime.now()
		print '-' * 50 + str(timespamp)

	except Exception, e:
		print str(e)


