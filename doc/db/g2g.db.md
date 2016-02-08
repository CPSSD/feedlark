
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
    _id: "devoxel"
    feeds: [ 
		{
        	feed = "https://news.ycombinator.com/rss",
        	name = "Bare Bones Back end",
        	link = "https://webkit.org/docs/b3/",
        	pub = Date("Mon, 8 Feb 2016 11:10:30 +0000")
    	}, 
    	{
        	feed = "https://news.ycombinator.com/rss",
        	name = "India bans discriminatory pricing based on source/destination/app/content",
        	link = "http://blog.savetheinternet.in/statement-on-trai-order-on-diff-pricing/",
        	pub_date = Date("Mon, 8 Feb 2016 11:44:22 +0000")
    	}, 	
	]
}
```