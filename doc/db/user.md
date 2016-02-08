User Database Specifications
===========================

The user database is the database that holds data individual to each user, including authentification data.

It interfaces with the secretary, and is used in combination with the Feed Database to create entries in the finished G2G database.


Example Document
----------------

```js
{
	_id: ObjectId("5099803df3f4948bd2f98391")
	username: "iandioch"
	hashed_password: "IjZAgcfl7p92ldGxad68LJZdL17lhWy"
	password_salt: "N9qo8uLOickgx2ZMRZoMye"
	subscribed_feeds: ["news.ycombinator.com/rss", "pssd.computing.dcu.ie/rss.xml"]
	
}
```
