#!/usr/bin/python
#-*- coding: UTF-8 -*-
 
import tweepy
import bitly_api
import sys, pickle, re, datetime, time
import urllib2
from urllib2 import urlopen, Request, HTTPError
from bs4 import BeautifulSoup
from bs4 import SoupStrainer



# twitter API
CONSUMER_KEY = 'Your Consumer Key'
CONSUMER_SECRET = 'Your Consumer Secret'
ACCESS_KEY = 'Your Access Key'
ACCESS_SECRET = 'Your Access Secret'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)



class Bibliomaniac: # class for query switcher / article list bindier

    def __init__(self, name):
        self.name = name
        self.routes = []

    def checkArticle(self, keyword):
        #proxy = urllib2.ProxyHandler({'http': '211.42.249.146:3128'})
        #opener = urllib2.build_opener(proxy)
        #urllib2.install_opener(opener)

        url = 'http://www.ilbe.com/ilbe'
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}
        htmltext = urlopen(Request(url, headers=headers))
        soup = BeautifulSoup(htmltext, parse_only = SoupStrainer('td', class_ = re.compile('title'))) # Analyze only filtered tags

        print '>' * 50 + 'Checking articles...'
        
        for e in soup.find_all('td', class_ = re.compile('title')):

            if e.strong and (keyword in e.strong):
                url = e.a.get('href') # type(url) == unicode
                title = e.a.get_text() # type(title) == unicode

                if [title, url] in (self.record or self.basket):
                    print '-' * 50 + 'Old one, already twitted.'
                    pass
                else:
                    self.basket.insert(0, [title, url])
                    print '+' * 50 + 'Found one!, sent buffer...'
            else: pass



class DumpTruck(Bibliomaniac):

    def __init__(self, name):
        Bibliomaniac.__init__(self, name)
    
    def makeFilter(self): # Turn key method
        with open(self.name + '_record.bin', 'wb') as f_f:
            pickle.dump(self.routes, f_f)

    def processArticle(self):
        with open(self.name + '_record.bin', 'rb') as f_f:
            self.record = pickle.load(f_f)
            self.checkArticle(self.keyword)

            for e in self.basket: # Update record
                self.record.insert(0, e)

        with open(self.name + '_record.bin', 'wb') as f_f:
            pickle.dump(self.record, f_f)
            print ' ' * 50 + 'Updated _record.bin.'



class BabyBird(DumpTruck):

    def __init__(self, name, keyword):
        DumpTruck.__init__(self, name)
        self.keyword = keyword
        self.basket = []

    # bit.ly API
    def shortenUrl(self, longurl):
        API_USER = 'Your API User'
        API_KEY = 'Your API Key'
        b = bitly_api.Connection(access_token = API_KEY)
        
        response = b.shorten(uri = longurl)
        shortUrl = response['url']

        return shortUrl

    def tweetMsg(self, e_arg):
        api.update_status(e_arg)
        
        try:
             print 'Tweet! : ' + e_arg
        
        except Exception, err:
             print str(err) 

    def feedBird(self): # Core; Scrap recent list - Filter - Refine message - Hand over bullet
        self.processArticle()
        print ' ' * 50 + 'processArticle() Success'

        try:
            if self.basket != []:
                for i in self.basket:
                    e_arg = i[0].encode('UTF-8') + ' ' +  self.shortenUrl(i[1]).encode('UTF-8') # encode when you moving around 'unicode + int' list or etc.
                    e_arg = e_arg[0:138] # Twitter allows only char 140
                    self.tweetMsg(e_arg)
                    time.sleep(5)
            
            else:
                print ' ' * 50 + 'Nothing in buffer.'
        
        except Exception, err:
            print str(err)

    def checkBroken(self):
        status = api.home_timeline() # Pull 20 tweets.
        for e in range(0, 20, 3):
            try:
                url = re.search(ur'(https:\/\/.*)', status[e].text.encode('UTF-8')).group(0)
                headers = {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}
                htmltext = urlopen(Request(urlopen(url).geturl(), headers=headers))
                soup = BeautifulSoup(htmltext, parse_only = SoupStrainer('div', class_ = re.compile('tCenter messageBox'))) # Check the status.
                if soup.div:
                    api.destroy_status(status[e].id)
                    print '!' * 50 + 'Deleted!, removed tweet...'
                else:
                    print '-' * 50 + 'Not deleted.'
            except Exception, err:
                print str(err)
            time.sleep(3)
        print ' ' * 50 + 'checkBroken() Success.'



if __name__ == '__main__':
    try:
        arabotja = BabyBird('ilbe', u'정보')
        # arabotja.makeFilter()
        arabotja.feedBird()
        arabotja.checkBroken()
        timestamp = datetime.datetime.now()
        print '<' * 50 + str(timestamp)
    
    except Exception, err:
        print str(err)
