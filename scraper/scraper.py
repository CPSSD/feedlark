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
        feed = feedparser.parse(rss_url)
        link_text = self._parse_from_web(feed["entries"][0]["links"][0]["href"])
        return link_text

    def _parse_from_web(self, article_url):
        r = requests.get(article_url)
        soup = BeautifulSoup(r.content,"html.parser")
        return soup.get_text().encode('utf-8')

#scr = Scraper()
#print(scr.get_feed_data("http://matt.might.net/articles/feed.rss"))

