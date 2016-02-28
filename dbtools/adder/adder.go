package adder

import (
	"fmt"
	"time"

	"github.com/mikespook/gearman-go/worker"
	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
)

func log(level int, s string) {
	//level 0 = INFO
	//level 1 = WARNING
	//level 2 = ERROR
	now := time.Now().Format("15:04:05 02/01/2006")

	levels := []string{"INFO", "WARNING", "ERROR"}
	fmt.Printf("%s %s: %s\n", now, levels[level], s)
}

func Create() error {
	// Create the worker and connect it to Gearman

	log(0, "Creating Gearman workers 'db-add' and 'db-update'")
	//	fmt.Println("Creating Gearman worker 'db-add' & 'db-update'")
	w := worker.New(worker.OneByOne)
	w.ErrorHandler = func(e error) {
		fmt.Println(e)
	}
	w.AddServer("tcp4", "127.0.0.1:4730")
	//	fmt.Println("Adding 'db-add' function.")
	w.AddFunc("db-add", DbAdd, worker.Unlimited)
	//	fmt.Println("Adding 'db-update' function.")
	w.AddFunc("db-update", DbUpdate, worker.Unlimited)
	//	fmt.Println("Adding 'db-upsert' function.")
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
	//	log(0, "Creating session.")
	session, _ := mgo.Dial(url)
	return session.DB(database).C(collection)
}

func AddDocument(dbUrl, database, collection string, jsonData bson.M) ([]byte, error) {
	// Add a document to the specified db & collection with the given data
	//	fmt.Println("Adding document to db " + database + " collection " + collection)
	log(0, "Adding document to db "+database+" collection "+collection)
	id, alreadyHasId := jsonData["_id"]
	if !alreadyHasId {
		id = bson.NewObjectId()
		jsonData["_id"] = id
	}
	coll := CreateSession(dbUrl, database, collection)
	err := coll.Insert(jsonData)
	if err != nil {
		log(1, err.Error())
		//fmt.Println(err)
	}
	response := bson.M{"status": "ok", "_id": id}
	bson, _ := bson.Marshal(response)
	return bson, err
}

func UpdateDocument(dbUrl, database, collection string, jsonData bson.M) ([]byte, error) {
	// Update a single document that matches the data in the selector{} with the updates given in updates{} (selector & updates taken from jsonData)
	//fmt.Println("Updating document in db " + database + " collection " + collection)
	log(0, "Updating document in db "+database+" collection "+collection)
	coll := CreateSession(dbUrl, database, collection)
	err := coll.Update(jsonData["selector"], jsonData["updates"])
	if err != nil {
		log(2, err.Error())
		//		fmt.Println(err)
	}
	response := bson.M{"status": "ok"}
	bson, _ := bson.Marshal(response)
	return bson, err
}

func UpsertDocument(dbUrl, database, collection string, jsonData bson.M) ([]byte, error) {
	//fmt.Println("Upserting document in db " + database + " collection " + collection)
	log(0, "Upserting document in db "+database+" collection "+collection)
	coll := CreateSession(dbUrl, database, collection)
	changeInfo, err := coll.Upsert(jsonData["selector"], jsonData["updates"])
	if err != nil {
		log(2, err.Error())
		//		fmt.Println(err)
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
	//fmt.Println("database adder called!")
	//fmt.Println(string(job.Data()))
	log(0, "Database adder called!")
	log(0, string(job.Data()))
	var data DbData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		//		fmt.Println(err)
		log(2, err.Error())
		return nil, err
	}
	//fmt.Println(data)
	//fmt.Println("Trying to add document to db")
	log(0, "Trying to add document to db")
	response, err := AddDocument("127.0.0.1:27017", data.Database, data.Collection, data.Data)
	if err != nil {
		log(1, err.Error())
		//fmt.Println(err)
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
		return nil, err
	}
	err = job.Err()
	return response, err
}

func DbUpdate(job worker.Job) ([]byte, error) {
	// a gearman wrapper for UpdateDocument
	//fmt.Println("database updater called!")
	log(0, "Database updater called!")
	var data DbData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		log(2, err.Error())
		//fmt.Println(err)
		return nil, err
	}
	//fmt.Println("DbUpdate data: ", data)
	response, err := UpdateDocument("127.0.0.1:27017", data.Database, data.Collection, data.Data)
	if err != nil {
		log(1, err.Error())
		//fmt.Println(err)
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
	}
	err = job.Err()
	return response, err
}

func DbUpsert(job worker.Job) ([]byte, error) {
	// a gearman wrapper for UpsertDocument
	//fmt.Println("database upserter called!")
	log(0, "Database upserter called!")
	var data DbData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		//fmt.Println(err)
		log(2, err.Error())
		return nil, err
	}
	fmt.Println("DbUpsert data: ", data)
	response, err := UpsertDocument("127.0.0.1:27017", data.Database, data.Collection, data.Data)
	if err != nil {
		log(1, err.Error())
		//fmt.Println(err)
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
	}
	err = job.Err()
	return response, err
}
