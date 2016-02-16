import sys
import requests
import feedparser
from bs4 import BeautifulSoup


#Ensure the class is used with Python 3 or greater.
assert sys.version_info >= (3,0)


class Scraper:
    def __init__(self):
        pass

    def get_feed_data(self, rss_url):
        '''
        Returns a list of dictionaries.
        Each dictionary corresponds to a item in the feed.

        The item contains a title, link, date published, and article text.
        '''
        if type(rss_url) != str:
            raise TypeError('URL must be a string')

        feed = feedparser.parse(rss_url)

        items_list = {"id" : rss_url,"database":"feeds","collection":"rss", "data": []}
        for item in feed['entries']:
            items_list["data"].append( {
                'title':item['title'],
                'link':item['link'],
                'pub_date':item['published'],
                'article_text':self._parse_from_web(item['link']),
                })

        return items_list

    def _parse_from_web(self, article_url):
        html = requests.get(article_url).content
        soup = BeautifulSoup(html,'html.parser')

        for s in soup(['style', 'script', '[document]', 'head', 'title']):
            s.extract()

        return soup.getText()

##scr = Scraper()
##for item in scr.get_feed_data("http://spritesmods.com/rss.php")["data"]:
##    print(item)
##    print()
