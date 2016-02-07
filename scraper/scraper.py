import sys
import requests
import feedparser
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        #Ensure the class is used with 3.5 or greater.
        assert sys.version_info >= (3,5)

    def get_feed_data(self, rss_url):
        pass

    def _parse_from_web(self, article_url):
        pass
