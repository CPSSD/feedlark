Opinion Updater
================

Dependencies
------------

- Python 2.7
- pymongo
- gearman
- Feedlark Adder
- Feedlark Getter

What is this?
-------------

This is the gearman worker that is called whenever a user likes or dislikes an article.

Usage
-----

The worker is called `register-vote`, and takes the following Gearman data:

```js
{
    "key": "secret_key_abc",
	"username": "iandioch",
	"feed_url": "http://news.ycombinator.com/rss",
	"article_url": "http://example.com/article",
	"positive_opinion": true
}
```

`username` should be the name of the user who just voted on an article. `feed_url` should be the url of the feed that article was taken from. `article_url` should be the link to that specific article. `positive_opinion` should be `true` if a user upvoted an article, and `false` if they downvoted it.


The worker just responds with the following:

```js
{
	"status":"success"
}
```

or 

```js
{
	"status":"error":
	"description":"error description"
}
```

How to do tests
---------------

The tests are written with the unittest module in python.

To run them make sure you have all the dependencies and the dbtools are running then run:

	$ python testing.py


To add unit tests modify the testing.py file.
Check out the unittest docs for examples and general help.
