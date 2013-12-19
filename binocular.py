#!/usr/bin/python
#-*- coding: UTF-8 -*-

import mechanize
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re
import time

class Bibliomaniac: # class for query switcher / article list bindier
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')]

	def __init__(self, name):
		self.name = name
		self.routes = []

	def loadTemplate(self, keyword, page):

		if self.name == 'google':
			self.url = 'http://www.google.com/'
			self.recipe = SoupStrainer('h3', class_ = 'r')
			[prefix, infix, suffix] = ['http://www.google.com/search?q=', '&start=', '']
			
			if page == 1:
				query = prefix + str(keyword) + infix + str(page - 1) + suffix
			else: 
				query = prefix + str(keyword) + infix + str((page - 1) * 10) + suffix
		
			return query

		elif self.name == 'ilbe':
			self.url = 'http://www.ilbe.com/'
			self.recipe = SoupStrainer('tr', class_ = re.compile('bg[12]')) # More information about this in official BeautifulSoup document
			[prefix, infix, suffix] = ['http://www.ilbe.com/?mid=ilbe&category=&search_target=title&&search_keyword=', '&page=', '']

			query = prefix + str(keyword) + infix + str(page) + suffix
		
			return query

		else:
			pass

	def bindPicture(self, keyword, lastpage): # Listing urls page by page

		try:
			page = 1
			keyword = keyword.replace(" ", "+")

			while page <= lastpage:
				query = self.loadTemplate(keyword, page)

				print 'Querying: ' + query
				
				htmltext = Bibliomaniac.br.open(query)
				soup = BeautifulSoup(htmltext, parse_only = self.recipe) # Analyze only filtered tags

				for e in soup.find_all('a'):
					url = e.get('href') # type(url) == unicode
					title = e.get_text() # type(title) == unicode
					self.routes.append([title, url])

				print str(page) + ' page done, Check ' + self.name + '.routes!'
				
				page += 1
				time.sleep(3)

		except Exception, e:
			print str(e)

	def getBackLost(self, keyword): # When backup server DB sleeping, retrieve the lost article

		page = self.url + self.name

		print '=' * 50 + 'Checking lost article...'
		
		htmltext = Bibliomaniac.br.open(page)
		soup = BeautifulSoup(htmltext, parse_only = self.recipe) # Analyze only filtered tags

		for e in soup.find_all('a'):
			url = e.get('href') # type(url) == unicode
			title = e.get_text() # type(title) == unicode
			
			if str(keyword) in title.encode('UTF-8'):

				if [title, url] in self.fineFilter or self.basket:
					print ' ' * 50 + 'Not a lost article!'
					pass
				
				else:
					self.basket.insert(0, [title, url])
					print '*' * 50 + 'Lost article!, Sent buffer.'
					print ' ' * 50 + 'Slow target server Warning!'
				
			else:
				pass


#Try this for test

#if __name__ == "__main__":
#	google = Bibliomaniac('google')
#	f = open(google.name + '_result.txt', 'w')
#	google.bindPicture('간철수', 2)
#	for q in google.routes:
#		for w in q:
#			for e in w:
#				p = e.encode('UTF-8')
#				f.write(p)
#				f.write('\n')
#			f.write('\n')
#			print ''
#		f.write('\n')
#		print ''
#	f.close()

#if __name__ == "__main__":
#	ilbe = Bibliomaniac('ilbe')
#	f = open(ilbe.name + '_result.txt', 'w')
#	ilbe.bindPicture('정보', 2)
#	for q in ilbe.routes:
#		for w in q:
#			for e in w:
#				print ilbe.routes
#				p = e.encode('UTF-8')
#				f.write(p)
#				f.write('\n')
#			f.write('\n')
#			print ''
#		f.write('\n')
#		print ''
#	f.close()


	
