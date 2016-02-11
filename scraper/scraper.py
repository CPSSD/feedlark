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
        all_rss = feed["entries"][0]
        name = all_rss['title']
        link = all_rss["link"]
        pub_date = all_rss["published"]
        link_text_content = self._parse_from_web(link)
        return link_text_content

    def _parse_from_web(self, article_url):
        r = requests.get(article_url)
        soup = BeautifulSoup(r.content,"html.parser")
        return soup.get_text(strip=True).encode('utf-8')

scr = Scraper()
print(scr.get_feed_data("https://news.ycombinator.com/rss"))
