User Database Specifications
===========================

The vote collection holds a log of all the votes by users on specific articles.

Example Document
----------------
```js
{
	"_id": ObjectId("5099803df3f4948bd2f98391"),
	"username": "iandioch",
	"article_url": "http://example.com/article",
	"feed_url":"https://news.ycombinator.com/rss",
	"positive_opinion":true
}
```

The `positive_opinion` field is `true` if a user upvoted an article, and `false` if they downvoted it.
