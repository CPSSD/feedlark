import requests
from bs4 import BeautifulSoup
import feedparser

feed = feedparser.parse("http://matt.might.net/articles/feed.rss")
#https://news.ycombinator.com/rss





def get_rss_html():
	# Goes through latest link for hacker news and gets html data from rss link.
	r = requests.get(feed["entries"][0]["links"][0]["href"])
	soup = BeautifulSoup(r.content,"html.parser")
	soup = soup.get_text()
	print(soup.encode("utf-8"))

	
def get_rss_html_for_all(): 
	#This will go through each link in the rss data of the website and get the html of the link in it.
	for i in range(len(feed["entries"])):
		r = requests.get(feed["entries"][0]["links"][0]["href"])
		soup = BeautifulSoup(r.content,"html.parser")
		soup = soup.get_text()
		print(soup.encode("utf-8"))
	
get_rss_html()


"""
# Finds specific tags in the html.
for link in soup.find_all('script'):
		print(link.encode("utf-8"))
"""
