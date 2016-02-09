
"G2G" Database Specifications
=============================

The `G2G Databse` is the database that consists of username keys and a
_sorted_ list of feeds. 

As feedlark is just doing RSS Aggregation at the moment, no data about
individual feeds is stored.


Example Document
----------------

```js
{
    username: "devoxel"
    feeds: [
        {
            feed = "https://news.ycombinator.com/rss",
            name = "Bare Bones Back end",
            link = "https://webkit.org/docs/b3/",
            pub_date = ISODate()
        },
        {
            feed = "https://news.ycombinator.com/rss",
            name = "India bans discriminatory pricing based on source/destination/app/content",
            link = "http://blog.savetheinternet.in/statement-on-trai-order-on-diff-pricing/",
            pub_date = ISODate()
        }
    ]
}
```
