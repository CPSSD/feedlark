Visualisation: Most Popular Feeds
=================================

This module will output statistics about the feeds that most users subscribe to.

Dependencies
------------

- Python 2.7


Usage
-----
To run this program the dbtools worker must be running to make the gearman calls.
Run `python popular_feeds.py X`, where X is the number of the most popular feeds you want the program to output data on. If this number is larger than the total number of feeds, the program will output data for every feed in the database.

The first line of the output is the number of feeds in the system. This is followed the top X most popular feeds in descending order in the following format:

`feed_name num_subscribers`

```
3
https://news.ycombinator.com/rss 100
http://spritesmods.com/rss.php 40
http://dave.cheney.net/feed 10
```

All of this data is computed at run-time, and is not cached, so might take some time.
