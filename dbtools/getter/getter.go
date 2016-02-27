package getter

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
	fmt.Println("Adding 'db-get' function.")
	w.AddFunc("db-get", DBGet, worker.Unlimited)
	if err := w.Ready(); err != nil {
		fmt.Println("Fatal error")
		fmt.Println(err)
		return err
	}
	w.Work()
	return nil
}

func CreateSession(url string, database string, collection string) *mgo.Collection {
	session, err := mgo.Dial(url)
	if err != nil {
		panic(err.Error())
	}
	return session.DB(database).C(collection)
}

type DBData struct {
	// the layout of a supplied document
	Database   string `bson:"database"`
	Collection string `bson:"collection"`
	Query      bson.M `bson:"query"`
	Projection bson.M `bson:"projection"`
}

func GetDocuments(dbUrl, database, collection string, query bson.M, projection bson.M) ([]byte, error) {
	fmt.Println("Getting documents from db " + database + " collection " + collection)
	coll := CreateSession(dbUrl, database, collection)
	var results []bson.M
	err := coll.Find(query).Select(projection).All(&results)
	if err != nil {
		fmt.Println("Could not iterate documents:" + err.Error())
		b, _ := bson.Marshal(bson.M{"status": "error", "error": err.Error()})
		return b, err
	}
	response := bson.M{"status": "ok", "docs": results}
	var bsonResponse []byte
	bsonResponse, err = bson.Marshal(response)
	if err != nil {
		fmt.Println("Could not marshal bson:" + err.Error())
		b, _ := bson.Marshal(bson.M{"status": "error", "description": err.Error()})
		return b, err
	}
	return bsonResponse, err
}

func DBGet(job worker.Job) ([]byte, error) {
	// a gearman wrapper for GetDocuments
	fmt.Println("database getter called!")
	var data DBData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		fmt.Println(err)
		return nil, err
	}
	fmt.Println("DBGet data: ", data)
	response, err := GetDocuments("127.0.0.1:27017", data.Database, data.Collection, data.Query, data.Projection)
	if err != nil {
		fmt.Println(err)
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
	}
	err = job.Err()
	return response, err
}
