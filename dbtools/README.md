Feedlark Database Adder
=======================

There are two elements to `dbtools`: `adder/adder.go`, and `getter/getter.go`. They are both written in Go, share the same dependencies, and can be run with `go run start_workers.go`.

They provide 4 Gearman workers: `db-get`, `db-add`, `db-update`, and `db-upsert`. The first is contained in `getter`, the other three in `adder`. Consult the individual README.md files in the directory of each to see the Gearman message specifications, and how to test each.

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

You can start the worker with `go run start_workers.go`


How to use
----------

See `getter/README.md` and `adder/README.md`.
