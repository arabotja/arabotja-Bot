arabotja-Bot
============

What is this?
------------
Ilbe informative article feeding Bot
(for personal python study)

About
------------
 - No DB authentication, access
 - 2 duplication-proof filters
 - Never miss vanishing article from target server search result database (v2.0~)
 - Flexibility of 'Filter size', 'Access timing' setting & 'Keyword chaging'
 - Classified modules for reorganizing the Bot (ex. Google searching)

Example
------------
 - Twitter: https://twitter.com/arabotja
 - Target site: http://www.ilbe.com/

Installation
------------

**You need python 2.7.6 and these python modules; BeautifulSoup4, mechanize, tweepy**

- Upload to your server
- Open arabotja.py 
- Apply your own bit.ly API, twitter API keys
- 'crontab -e' and set the target page access timing (Create log file by '>' operator) *google 'crontab' for more information*
- 'python arabotja_turnKey.py' for first initiation (or Reboot + Filter up-to-date reset)

etc.
------------
* License : MIT
* GitHub : https://github.com/arabotja/arabotja-Bot/
* E-mail : arabotja@gmail.com
