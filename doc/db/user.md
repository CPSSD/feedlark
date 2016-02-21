User Database Specifications
===========================

The user database is the database that holds data individual to each user,
including authentification data.

It interfaces with the secretary, and is used in combination with the Feed
Database to create entries in the finished G2G database.

The user password will not be stored, instead, a salt and the hashed password
and salt will be stored. These are stored in the same string in bcrypt.

Example Document
----------------
		password = "ilovegnuhurd", 8 rounds

```js
{
	"_id": ObjectId("5099803df3f4948bd2f98391"),
	"username": "iandioch",
	"email": "noah@feedlark.com",
	"password": "$2a$08$ThzPc3zm84JPb6LmvcfCkuXkwyh8H.Mn1VC4EKu9guksI9lbdb7Fa",
	"subscribed_feeds": ["news.ycombinator.com/rss", "pssd.computing.dcu.ie/rss.xml"]
}
```
