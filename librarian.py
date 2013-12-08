#!/usr/bin/python
#-*- coding: UTF-8 -*-

import pickle
from binocular import Bibliomaniac

class DumpTruck(Bibliomaniac):

	def __init__(self, name):
		Bibliomaniac.__init__(self, name)

	def makeFilter(self, keyword, lastpage): # When you turn key, recent article list become two filters' base
		self.bindPicture(keyword, lastpage)
	
		l_f = open(self.name + '_lightFilter.bin', 'wb') # l_f for light_file; Copying of last recent article list
		pickle.dump(self.routes, l_f)
		l_f.close()
		del l_f

		f_f = open(self.name + '_fineFilter.bin', 'wb') # f_f for fine_file; Incremental filter list from your turn key 
		pickle.dump(self.routes, f_f)
		f_f.close()
		del f_f
	
	def dumpRecent(self, keyword, lastpage):
		self.bindPicture(keyword, lastpage)
	
		r_f = open(self.name + '_recentTweet.bin', 'wb') # r_f for recent_file
		pickle.dump(self.routes, r_f)
		r_f.close()
		del r_f
	
	def judgeArticle(self): # Filter core

		r_f = open(self.name + '_recentTweet.bin', 'rb') 
		recentTweet = pickle.load(r_f)
		r_f.close()
		del r_f

		l_f = open(self.name + '_lightFilter.bin', 'rb') 
		lightFilter = pickle.load(l_f)
		l_f.close()
		del l_f

		f_f = open(self.name + '_fineFilter.bin', 'rb') 
		self.fineFilter = pickle.load(f_f)
		f_f.close()
		del f_f

		i = 0
		while i < 5: # Old one? or New one?
			
			if recentTweet[i] in lightFilter:
				print '-' * 50 + 'Old one...Already tweeted.'

			elif recentTweet[i] in self.fineFilter: # Server stuttering proof
				print '?' * 50 + 'Old one...Already tweeted. (Unstable Server Warning!!!)'

			else:
				self.basket.insert(0, recentTweet[i])
				print '+' * 50 + 'New article!, Sent buffer.'

			i += 1

		for e in self.basket: # Update fine filter
			self.fineFilter.insert(0, e)

		f_f = open(self.name + '_fineFilter.bin', 'wb')
		pickle.dump(self.fineFilter, f_f)
		f_f.close()
		del f_f
		print '-' * 50 + 'Updated _fineFilter.bin.'

		l_f = open(self.name + '_lightFilter.bin', 'wb') # Update light filter
		pickle.dump(recentTweet, l_f)
		l_f.close()
		del l_f
		print '-' * 50 + 'Updated _lightFilter.bin.'


