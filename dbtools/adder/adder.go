package adder

import (
	"fmt"

	"../dbhelp"
	"github.com/mikespook/gearman-go/worker"
	"gopkg.in/mgo.v2/bson"
)

func Create() error {
	// Create the worker and connect it to Gearman

	dbhelp.Log(0, "Creating Gearman workers 'db-add' and 'db-update'")
	w := worker.New(worker.OneByOne)
	w.ErrorHandler = func(e error) {
		fmt.Println(e)
	}
	w.AddServer("tcp4", "127.0.0.1:4730")
	w.AddFunc("db-add", DbAdd, worker.Unlimited)
	w.AddFunc("db-update", DbUpdate, worker.Unlimited)
	w.AddFunc("db-upsert", DbUpsert, worker.Unlimited)
	if err := w.Ready(); err != nil {
		fmt.Println("Fatal error")
		fmt.Println(err)
		return err
	}
	w.Work()
	return nil
}


func AddDocument(dbUrl, database, collection string, jsonData bson.M) ([]byte, error) {
	// Add a document to the specified db & collection with the given data
	dbhelp.Log(0, "Adding document to db "+database+" collection "+collection)
	id, alreadyHasId := jsonData["_id"]
	if !alreadyHasId {
		id = bson.NewObjectId()
		jsonData["_id"] = id
	}
	coll := dbhelp.CreateSession(dbUrl, database, collection)
	err := coll.Insert(jsonData)
	response := bson.M{"status": "ok", "_id": id}
	if err != nil {
		dbhelp.Log(1, err.Error())
		response = bson.M{"status": "error", "error": err.Error()}
	}
	bson, _ := bson.Marshal(response)
	coll.Database.Session.Close()
	return bson, err
}

func UpdateDocument(dbUrl, database, collection string, jsonData bson.M) ([]byte, error) {
	// Update a single document that matches the data in the selector{} with the updates given in updates{} (selector & updates taken from jsonData)
	dbhelp.Log(0, "Updating document in db "+database+" collection "+collection)
	coll := dbhelp.CreateSession(dbUrl, database, collection)
	err := coll.Update(jsonData["selector"], jsonData["updates"])
	response := bson.M{"status": "ok"}
	if err != nil {
		dbhelp.Log(2, err.Error())
		response = bson.M{"status": "error", "error": err.Error()}
	}
	bson, _ := bson.Marshal(response)
	coll.Database.Session.Close()
	return bson, err
}

func UpsertDocument(dbUrl, database, collection string, jsonData bson.M) ([]byte, error) {
	//fmt.Println("Upserting document in db " + database + " collection " + collection)
	dbhelp.Log(0, "Upserting document in db "+database+" collection "+collection)
	coll := dbhelp.CreateSession(dbUrl, database, collection)
	changeInfo, err := coll.Upsert(jsonData["selector"], jsonData["updates"])
	newDocCreated := changeInfo.Updated == 0
	response := bson.M{"status": "ok", "new_doc": newDocCreated}
	if err != nil {
		dbhelp.Log(2, err.Error())
		response = bson.M{"status": "error", "error": err.Error()}
	}
	bson, _ := bson.Marshal(response)
	coll.Database.Session.Close()
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
	dbhelp.Log(0, "Database adder called!")
	var data DbData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		dbhelp.Log(2, err.Error())
		return nil, err
	}
	url := dbhelp.GetURL()
	response, err := AddDocument(url, data.Database, data.Collection, data.Data)
	if err != nil {
		dbhelp.Log(1, err.Error())
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
		return nil, err
	}
	err = job.Err()
	return response, err
}

func DbUpdate(job worker.Job) ([]byte, error) {
	// a gearman wrapper for UpdateDocument
	dbhelp.Log(0, "Database updater called!")
	var data DbData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		dbhelp.Log(2, err.Error())
		return nil, err
	}
	url := dbhelp.GetURL()
	response, err := UpdateDocument(url, data.Database, data.Collection, data.Data)
	if err != nil {
		dbhelp.Log(1, err.Error())
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
	}
	err = job.Err()
	return response, err
}

func DbUpsert(job worker.Job) ([]byte, error) {
	// a gearman wrapper for UpsertDocument
	dbhelp.Log(0, "Database upserter called!")
	var data DbData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		dbhelp.Log(2, err.Error())
		return nil, err
	}
	url := dbhelp.GetURL()
	response, err := UpsertDocument(url, data.Database, data.Collection, data.Data)
	if err != nil {
		dbhelp.Log(1, err.Error())
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
	}
	err = job.Err()
	return response, err
}
