import requests
from bs4 import BeautifulSoup
import sys

#Ensure the class is used with a recent Python 2.
assert (2,5) <= sys.version_info <= (3,0)
class Article_getter:

    def __init__(self):
        pass

    def get_article_text(self, article_url):
        if type(article_url) != str and type(article_url) != unicode:
            raise TypeError('URL must be a string')
            return 'URL must be a string'

        html = requests.get(article_url).content
        soup = BeautifulSoup(html,'html.parser')

        for s in soup(['style', 'script', '[document]', 'head', 'title']):
            s.extract()

        return soup.getText().strip().encode("utf-8")
