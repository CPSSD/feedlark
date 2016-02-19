
"G2G" Database Specifications
=============================

The `G2G Database` is the database that consists of username keys and a
_sorted_ list of feeds.

As feedlark is just doing RSS Aggregation at the moment, no data about
individual feeds is stored.


Example Document
----------------

```js
{
    "username": "devoxel"
    "feeds": [
        {
            "feed" : "https://news.ycombinator.com/rss",
            "name" : "Bare Bones Back end",
            "link" : "https://webkit.org/docs/b3/",
            "pub_date" : "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=10, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)"
        },
        {
            "feed" : "https://news.ycombinator.com/rss",
            "name" : "India bans discriminatory pricing based on source/destination/app/content",
            "link" : "http://blog.savetheinternet.in/statement-on-trai-order-on-diff-pricing/",
            "pub_date" : "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=10, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)"
        }
    ]
}
```
