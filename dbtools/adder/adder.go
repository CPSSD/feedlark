package adder

import (
	"fmt"
	"github.com/mikespook/gearman-go/worker"
	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
)

func Create() error {
	// Create the worker and connect it to Gearman

	fmt.Println("Creating Gearman worker 'db-add' & 'db-update'")
	w := worker.New(worker.OneByOne)
	w.ErrorHandler = func(e error) {
		fmt.Println(e)
	}
	w.AddServer("tcp4", "127.0.0.1:4730")
	fmt.Println("Adding 'db-add' function.")
	w.AddFunc("db-add", DbAdd, worker.Unlimited)
	fmt.Println("Adding 'db-update' function.")
	w.AddFunc("db-update", DbUpdate, worker.Unlimited)
	fmt.Println("Adding 'db-upsert' function.")
	w.AddFunc("db-upsert", DbUpsert, worker.Unlimited)
	if err := w.Ready(); err != nil {
		fmt.Println("Fatal error")
		fmt.Println(err)
		return err
	}
	w.Work()
	return nil
}

func CreateSession(url string, database string, collection string) *mgo.Collection {
	session, _ := mgo.Dial(url)
	return session.DB(database).C(collection)
}

func AddDocument(dbUrl, database, collection string, jsonData bson.M) ([]byte, error) {
	// Add a document to the specified db & collection with the given data
	fmt.Println("Adding document to db " + database + " collection " + collection)
	id, alreadyHasId := jsonData["_id"]
	if !alreadyHasId {
		id = bson.NewObjectId()
		jsonData["_id"] = id
	}
	coll := CreateSession(dbUrl, database, collection)
	err := coll.Insert(jsonData)
	if err != nil {
		fmt.Println(err)
	}
	response := bson.M{"status": "ok", "_id": id}
	bson, _ := bson.Marshal(response)
	return bson, err
}

func UpdateDocument(dbUrl, database, collection string, jsonData bson.M) ([]byte, error) {
	// Update a single document that matches the data in the selector{} with the updates given in updates{} (selector & updates taken from jsonData)
	fmt.Println("Updating document in db " + database + " collection " + collection)
	coll := CreateSession(dbUrl, database, collection)
	err := coll.Update(jsonData["selector"], jsonData["updates"])
	if err != nil {
		fmt.Println(err)
	}
	response := bson.M{"status": "ok"}
	bson, _ := bson.Marshal(response)
	return bson, err
}

func UpsertDocument(dbUrl, database, collection string, jsonData bson.M) ([]byte, error) {
	fmt.Println("Upserting document in db " + database + " collection " + collection)
	coll := CreateSession(dbUrl, database, collection)
	changeInfo, err := coll.Upsert(jsonData["selector"], jsonData["updates"])
	if err != nil {
		fmt.Println(err)
	}
	newDocCreated := changeInfo.Updated == 0
	response := bson.M{"status": "ok", "new_doc": newDocCreated}
	bson, _ := bson.Marshal(response)
	return bson, err
}

type DbData struct {
	// the layout of a supplied document
	Database   string `bson:"database"`
	Collection string `bson:"collection"`
	Data       bson.M `bson:"data"`
}

func DbAdd(job worker.Job) ([]byte, error) {
	// a gearman wrapper for AddDocument
	fmt.Println("database adder called!")
	fmt.Println(string(job.Data()))
	var data DbData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		fmt.Println(err)
		return nil, err
	}
	fmt.Println(data)
	fmt.Println("Trying to add document to db")
	response, err := AddDocument("127.0.0.1:27017", data.Database, data.Collection, data.Data)
	if err != nil {
		fmt.Println(err)
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
		return nil, err
	}
	err = job.Err()
	return response, err
}

func DbUpdate(job worker.Job) ([]byte, error) {
	// a gearman wrapper for UpdateDocument
	fmt.Println("database updater called!")
	var data DbData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		fmt.Println(err)
		return nil, err
	}
	fmt.Println("DbUpdate data: ", data)
	response, err := UpdateDocument("127.0.0.1:27017", data.Database, data.Collection, data.Data)
	if err != nil {
		fmt.Println(err)
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
	}
	err = job.Err()
	return response, err
}

func DbUpsert(job worker.Job) ([]byte, error) {
	// a gearman wrapper for UpsertDocument
	fmt.Println("database upserter called!")
	var data DbData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		fmt.Println(err)
		return nil, err
	}
	fmt.Println("DbUpsert data: ", data)
	response, err := UpsertDocument("127.0.0.1:27017", data.Database, data.Collection, data.Data)
	if err != nil {
		fmt.Println(err)
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
	}
	err = job.Err()
	return response, err
}
