#!/usr/bin/python
#-*- coding: UTF-8 -*-
 
import tweepy
import bitly_api
import sys, pickle, time, datetime
import re
from librarian import DumpTruck
from maintenance import Repairman
 
# twitter API
CONSUMER_KEY = 'yourConsumerKey'
CONSUMER_SECRET = 'yourConsumerSecret'
ACCESS_KEY = 'yourAccessKey'
ACCESS_SECRET = 'yourAccessSecret'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class BabyBird(DumpTruck, Repairman):

	def __init__(self, name, keyword):
		DumpTruck.__init__(self, name)
		self.keyword = keyword
		self.basket = []

	# bit.ly API
	def shortenUrl(self,longurl):
		API_USER = "yourUsername"
		API_KEY = "yourAPIKey"
		b = bitly_api.Connection(access_token = API_KEY)
		
		response = b.shorten(uri = longurl)
		shortUrl = response['url']

		return shortUrl

	def tweetMsg(self, e_arg):
		api.update_status(e_arg)
		
		try:
		 	print 'Tweet! : ' + e_arg
		
		except Exception, e:
		 	print str(e) 

	def wakeBird(self): # Turn key for first start or reboot (small DB making to prevent duplication)
		self.makeFilter(self.keyword, 3)
		print '~' * 50 + 'makeFilter() Success'

	def feedBird(self): # Core; Scrap recent list - Filter - Refine message - Hand over bullet
		self.dumpRecent(self.keyword, 1)
		print '~' * 50 + 'dumpRecent() Success'
		self.judgeArticle()
		print ' ' * 50 + 'judgeArticle() Success'

		try:
			if self.basket != []:
				for i in self.basket:
					e_arg = i[0].encode('UTF-8') + ' ' +  self.shortenUrl(i[1]).encode('UTF-8') # encode when you moving around 'unicode + int' list or etc.
					e_arg = e_arg[0:138] # Twitter allows only char 140
					self.tweetMsg(e_arg)
					time.sleep(5)
			
			else:
				print ' ' * 50 + 'Nothing in buffer.'
		
		except Exception, e:
			print str(e)



if __name__ == '__main__':
	try:
		arabotja = BabyBird('ilbe', '정보')
		arabotja.feedBird()
		timespamp = datetime.datetime.now()
		print '~' * 50 + str(timespamp)
	
	except Exception, e:
		print str(e)


