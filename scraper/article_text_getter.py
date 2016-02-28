import requests
from bs4 import BeautifulSoup
import sys

#Ensure the class is used with a recent Python 2.
assert (2,5) <= sys.version_info <= (3,0)

class Text_scraper:

    def get_article_text(self, article_url):
        html = requests.get(article_url).content
        soup = BeautifulSoup(html,'html.parser')

        for s in soup(['style', 'script', '[document]', 'head', 'title']):
            s.extract()

        text = soup.getText().strip()
        return "".join([s for s in text.splitlines(True) if s.strip("\r\n")]).encode("utf-8")
