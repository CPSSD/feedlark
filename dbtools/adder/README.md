Feedlark Database Adder
=======================

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
    "key": "the_crow_flies_at_midnight",
    "database":"feedlark",
    "collection":"feed",
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
    "key": "never_gonna_give_u_up",
    "database":"feedlark",
    "collection":"feed",
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

The `db-upsert` tool expects this data:

```js
{
    "key": "upsert_this",
    "database":"feedlark",    
    "collection":"feed",
    "data":{
        "updates":{
            "dank":"cave"
        }
        "selector":{
            "dank":"meme"
        }
    }
}
```

It will see if a document exists with the given query and update it. If no such document exists, it will update the data in `selector` with the data in `updates` and put that in the database as a new document. It returns the following data:

```js
{
    "status":"ok"
    "new_doc":true
}
```

`new_doc` will be `true` if the upsert function resulted in the creation of a new document, and `false` if it updated a pre-existing document.
