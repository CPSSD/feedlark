Feedlark Database Adder
=======================

Dependencies
------------

- Go v1.5
- https://github.com/mikespook/gearman-go
- http://labix.org/mgo


How to set up your environment
------------------------------

Make sure the `$GOPATH` is set.

```go
go get "github.com/mikespook/gearman-go/worker"
go get "gopkg.in/mgo.v2"
go get "gopkg.in/mgo.v2/bson"
```

You can start the worker with `go run ../start_workers.go`

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
