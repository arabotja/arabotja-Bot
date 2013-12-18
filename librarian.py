#!/usr/bin/python
#-*- coding: UTF-8 -*-

import pickle
from binocular import Bibliomaniac

class DumpTruck(Bibliomaniac):

	def __init__(self, name):
		Bibliomaniac.__init__(self, name)

	def makeFilter(self, keyword, lastpage): # When you turn key, recent article list become two filters' base
		self.bindPicture(keyword, lastpage)

		self.routes = self.fixList(self.routes)

		with open(self.name + '_lightFilter.bin', 'wb') as l_f, open(self.name + '_fineFilter.bin', 'wb') as f_f:
			pickle.dump(self.routes, l_f)
			pickle.dump(self.routes, f_f)
	
	def dumpRecent(self, keyword, lastpage):
		self.bindPicture(keyword, lastpage)

		self.routes = self.fixList(self.routes)
	
		with open(self.name + '_recentTweet.bin', 'wb') as r_f:
			pickle.dump(self.routes, r_f)
	
	def judgeArticle(self): # Filter core

		with open(self.name + '_recentTweet.bin', 'rb') as r_f, open(self.name + '_lightFilter.bin', 'rb') as l_f, open(self.name + '_fineFilter.bin', 'rb') as f_f:
			recentTweet = pickle.load(r_f)
			lightFilter = pickle.load(l_f)
			self.fineFilter = pickle.load(f_f)

		i = 0
		while i < 5: # Old one? or New one?
			
			if recentTweet[i] in lightFilter:
				print ' ' * 50 + 'Old one...Already tweeted.'

			elif recentTweet[i] in self.fineFilter: # Server stuttering situation procedure
				print '?' * 50 + 'Old one...Already tweeted.'
				print ' ' * 50 + 'Unstable Server Warning!!!'

			else:
				self.basket.insert(0, recentTweet[i])
				print '+' * 50 + 'New article!, Sent buffer.'

			i += 1

		self.getBackLost(self.keyword)

		for e in self.basket: # Update fine filter
			self.fineFilter.insert(0, e)

		with open(self.name + '_fineFilter.bin', 'wb') as f_f, open(self.name + '_lightFilter.bin', 'wb') as l_f:
			pickle.dump(self.fineFilter, f_f)
			print ' ' * 50 + 'Updated _fineFilter.bin.'
			pickle.dump(recentTweet, l_f)
			print ' ' * 50 + 'Updated _lightFilter.bin.'


