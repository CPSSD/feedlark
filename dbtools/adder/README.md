Feedlark Database Adder
=======================

Dependencies
------------

- Go v1.5
- https://github.com/mikespook/gearman-go
- http://labix.org/mgo


How to set up your environment
------------------------------

Running `go get` in the dir the file is in supposedly adds the required libraries to the environment, but it gives errors for me about the $GOPATH. However, `go run adder.go` still works; I need to investigate this further, but it may be easier to trace the problem on a fresh go install.

How to do tests
---------------

`cd` to this directory, and run `go test`

How to use
----------

All communications are in BSON.

The `db-add` tool expects you to give it gearman data formatted like this:

```js
{
    "database":"feeds",
    "collection":"rss",
    "data":{
        "dank":"memes"   
    }
}
```

It will return some BSON like this, containing the id of the newly added file:

```js
{
    "status": "ok",
    "_id": ObjectId(000000000000)
}
```

The `db-update` tool expects you to give it gearman data formatted like this:

```js
{
    "database":"feeds",
    "collection":"rss",
    "data":{
        "updates":{
            "dank":"cave"
        },
        "selector":{
            "_id":ObjectId(000000000000)
        }
    }
}
```

It will update a single document that matches the data you give it in `selector`, with the given data in `updates`, and return the following:

```js
{
    "status":"ok"
}
```
