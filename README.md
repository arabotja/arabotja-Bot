arabotja-Bot
============

What is this?
------------
Ilbe informative article feeding twitter Bot(for personal python study)

About
------------
 - No DB authentication, access
 - Flexibility of 'Access timing' & 'Keyword chaging'
 - Simplified code(much better than v2.x)
 - If you want more expandability(like 'random old article review', 'google search', etc.), try v2.x version instead of v3.x

Example
------------
 - Twitter: https://twitter.com/arabotja
 - Target site: http://www.ilbe.com/

Installation
------------
**You need python 2.7.6 and these external python modules; BeautifulSoup4, mechanize, tweepy**

- Upload arabotja.py to your server
- Open arabotja.py with vim or else 
- Apply your own bit.ly API, twitter API keys
- 'crontab -e' and set the target page access timing (Create log file by '>' operator) *google 'crontab' for more information*
- Try 'self.makeFilter()' method at first to create _record.bin file

etc.
------------
* License : MIT(https://github.com/arabotja/arabotja-Bot/blob/master/LICENSE)
* GitHub : https://github.com/arabotja/arabotja-Bot/
* E-mail : arabotja@gmail.com
