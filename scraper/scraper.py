import sys
import requests
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
from article_text_getter import Text_scraper


#Ensure the class is used with a recent Python 2.
assert (2,5) <= sys.version_info <= (3,0)


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
        text_getter = Text_scraper()
        feed = feedparser.parse(rss_url)
        items_list = []
        for item in feed['entries']:
            date = item['published_parsed'] if 'published_parsed' in item else item['updated_parsed']
            items_list.append({
                'name':item['title'],
                'link':item['link'],
                'pub_date':datetime(*date[:6]),
                'article_text': text_getter.get_article_text(item['link'])
                })
        return items_list
