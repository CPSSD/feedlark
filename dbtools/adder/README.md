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
Move to this directory, and run `go test`


How to use
----------

The `db-add` tool expects you to give it gearman data formatted like this:
```js
    "database":"feeds",
    "collection":"rss",
    "data":{
        "dank":"memes"   
    }
```

The `db-update` tool expects you to give it gearman data formatted like this:
```js
    "database":"feeds",
    "collection":"rss",
    "data":{
        "updates":{
            "dank":"cave"
        },
        "id":ObjectId(000000000000)
    }
```
