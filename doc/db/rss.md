# RSS/ATOM Feed Database Specifications

The Feed database is the database which holds the url of the website as the key, the rss/atom data and the article data.

It will interface with the Scraper, Catagoriser, Secretary and the feed aggregator.

## Example Document:
```js
{
  url: "https://news.ycombinator.com/rss",
  feeds: [
      {
          name: "How Feedlark made the first nullion",
          pub_date: ISODate(),
          link: "https://www.rte.ie/feedlark"
          arictle_text: "Lotta compliments to founders."
      },
      {
          name: "How Lua ruined the world",
          pub_date: ISODate(),
          link: "https://www.doomsdayclock.com/lua",
          article_text: "Good old fashioned Lua bashing."
        }
    ]

}
```
