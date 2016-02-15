package adder

import (
	"encoding/json"
	"fmt"
	"github.com/mikespook/gearman-go/worker"
	"gopkg.in/mgo.v2"
)

func Create() error {
	fmt.Println("Creating Gearman worker 'db-add'")
	w := worker.New(worker.OneByOne)
	w.ErrorHandler = func(e error) {
		fmt.Println(e)
	}
	w.AddServer("tcp4", "127.0.0.1:4730")
	w.AddFunc("db-add", DbAdd, worker.Unlimited)
	w.AddFunc("db-update", DbUpdate, worker.Unlimited)
	if err := w.Ready(); err != nil {
		fmt.Println("Fatal error")
		fmt.Println(err)
		return err
	}
	go w.Work()
	return nil
}

func CreateSession(url string, database string, collection string) *mgo.Collection {
	session, _ := mgo.Dial(url)
	return session.DB(database).C(collection)
}

func AddDocument(dbUrl, database, collection, jsonData string) error {
	coll := CreateSession(dbUrl, database, collection)
	err := coll.Insert(jsonData)
	return err
}

type DbData struct {
	Database   string `json:"database"`
	Collection string `json:"collection"`
	Data       string `json:"data"`
}

func DbAdd(job worker.Job) ([]byte, error) {
	fmt.Println("database adder called!")
	var data DbData
	if err := json.Unmarshal(job.Data(), &data); err != nil {
		return nil, err
	}
	err := AddDocument("127.0.0.1:27017", data.Database, data.Collection, data.Data)
	if err != nil {
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
		return nil, err
	}
	err = job.Err()
	return nil, err
}
