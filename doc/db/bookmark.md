"Bookmark" Database Specifications
=============================

The `Bookmark Database` is the database that stores feeds that the user has selected to be saved.

Each saved article holds the title of the article, a link to the feed it was scraped from, the
link to the actual article and the date it was published.

Example Document
----------------

```js
{
    "_id" : ObjectId("57127893622eef7fefc337ce"),
    "username" : "theotherguys",
    "bookmarks" : [
        {
            "feed" : "http://www.rte.ie/news/rss/news-headlines.xml",
            "name" : "Oxfam accuses EU of failing to protect migrants",
            "link" : "http://www.rte.ie/news/2016/0418/782505-oxfam-eu-migrants/",
            "date" : "2016-04-18"
        }
    ]
}
{
    "_id" : ObjectId("571368b752754c2f090aeea2"),
    "username" : "sully",
    "bookmarks" : [
        {
            "feed" : "http://www.rte.ie/news/rss/news-headlines.xml",
            "name" : "News in Brief",
            "link" : "http://www.rte.ie/news/2016/0418/782533-oscar-pistorius-sentencing/",
            "date" : "2016-04-18"
        },
        {
            "feed" : "http://www.rte.ie/news/rss/news-headlines.xml",
            "name" : "Derry nun among 272 dead in Ecuador earthquake",
            "link" : "http://www.rte.ie/news/2016/0418/782504-ecuador-earthquake-death-toll/",
            "date" : "2016-04-18"
        }
    ]
}
```
