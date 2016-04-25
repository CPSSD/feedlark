package getter

import (
	"fmt"

	"../dbhelp"
	"github.com/mikespook/gearman-go/worker"
	"gopkg.in/mgo.v2/bson"
)

func Create() error {
	// Create the worker and connect it to Gearman

	dbhelp.Log(0, "Creating Gearman worker 'db-get'")
	w := worker.New(worker.OneByOne)
	w.ErrorHandler = func(e error) {
		fmt.Println(e)
	}
	w.AddServer("tcp4", "127.0.0.1:4730")
	w.AddFunc("db-get", DBGet, worker.Unlimited)
	if err := w.Ready(); err != nil {
		dbhelp.Log(2, "Fatal error: "+err.Error())
		return err
	}
	w.Work()
	return nil
}

type DBData struct {
	// the layout of a supplied document
	Key        string `bson:"key"`
	Database   string `bson:"database"`
	Collection string `bson:"collection"`
	Query      bson.M `bson:"query"`
	Projection bson.M `bson:"projection"`
}

func GetDocuments(dbUrl, database, collection string, query bson.M, projection bson.M) ([]byte, error) {
	dbhelp.Log(0, "Getting documents from db "+database+" collection "+collection)
	coll := dbhelp.CreateSession(dbUrl, database, collection)
	var results []bson.M
	err := coll.Find(query).Select(projection).All(&results)
	if err != nil {
		dbhelp.Log(2, "Could not iterate documents: "+err.Error())
		b, _ := bson.Marshal(bson.M{"status": "error", "error": err.Error()})
		return b, err
	}
	response := bson.M{"status": "ok", "docs": results}
	var bsonResponse []byte
	bsonResponse, err = bson.Marshal(response)
	if err != nil {
		dbhelp.Log(2, "Could not marshal bson: "+err.Error())
		b, _ := bson.Marshal(bson.M{"status": "error", "description": err.Error()})
		return b, err
	}
	coll.Database.Session.Close()
	return bsonResponse, err
}

func DBGet(job worker.Job) ([]byte, error) {
	// a gearman wrapper for GetDocuments
	dbhelp.Log(0, "Database getter called!")
	var data DBData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		dbhelp.Log(2, err.Error())
		return nil, err
	}
    if !dbhelp.CorrectKey(data.Key) {
        dbhelp.Log(2, "Secret key mismatch")
        b, _ := bson.Marshal(bson.M{"status": "error", "description": "Secret key mismatch"})
        return b, job.Err()
    }
	url := dbhelp.GetURL()
	response, err := GetDocuments(url, data.Database, data.Collection, data.Query, data.Projection)
	if err != nil {
		dbhelp.Log(1, err.Error())
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
	}
	err = job.Err()
	return response, err
}
