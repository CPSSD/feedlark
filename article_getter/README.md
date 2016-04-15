Feedlark:tm: Article_getter
================

Dependencies
------------

- Python 2.7
- pip
- requests
- bson
- datetime
- sys
- gearman
- requests
- BeautifulSoup

How to run
------------
To run the article getter you must submit a job to the gearman article-text-getter worker with the bson object of the url of the feed you want to get the articles for.
Below is an example of how to do this.

```
text_getter_data = str(bson.BSON.encode({
    "key": "secret_key_abc",
    "url": "http://www.feedurltoscrape.com",
    }))
gm_client.submit_job('article-text-getter',text_getter_data, background=True)
```

This will return a bson string with a status field and a updated_feed or an error-descrition field.
* Status "ok" if there are no issues
```js
{
    "key": "secret_key_abc",
    "status":"ok",
    "updated_feed": feed_db_data['_id'],
}
```

* Status "error" for any issues.
```js
{
    "status": "error",
    "error-description": "Error message",
}
```


How to do tests
------------

The tests are written with the unittest module in python. Navigate to the article_getter directory and run the following command to start testing.

	python testing.py

To add unit tests modify the testing.py file.
Check out the unittest docs for examples and general help.
