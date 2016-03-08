package getter

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

	log(0, "Creating Gearman worker 'db-get'")
	w := worker.New(worker.OneByOne)
	w.ErrorHandler = func(e error) {
		fmt.Println(e)
	}
	w.AddServer("tcp4", "127.0.0.1:4730")
	w.AddFunc("db-get", DBGet, worker.Unlimited)
	if err := w.Ready(); err != nil {
		log(2, "Fatal error: "+err.Error())
		return err
	}
	w.Work()
	return nil
}

func CreateSession(url string, database string, collection string) *mgo.Collection {
	session, err := mgo.Dial(url)
	if err != nil {
		log(2, err.Error())
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
	log(0, "Getting documents from db "+database+" collection "+collection)
	coll := CreateSession(dbUrl, database, collection)
	var results []bson.M
	err := coll.Find(query).Select(projection).All(&results)
	if err != nil {
		log(2, "Could not iterate documents: "+err.Error())
		b, _ := bson.Marshal(bson.M{"status": "error", "error": err.Error()})
		return b, err
	}
	response := bson.M{"status": "ok", "docs": results}
	var bsonResponse []byte
	bsonResponse, err = bson.Marshal(response)
	if err != nil {
		log(2, "Could not marshal bson: "+err.Error())
		b, _ := bson.Marshal(bson.M{"status": "error", "description": err.Error()})
		return b, err
	}
	return bsonResponse, err
}

func DBGet(job worker.Job) ([]byte, error) {
	// a gearman wrapper for GetDocuments
	log(0, "Database getter called!")
	var data DBData
	if err := bson.Unmarshal(job.Data(), &data); err != nil {
		log(2, err.Error())
		return nil, err
	}
	response, err := GetDocuments("127.0.0.1:27017", data.Database, data.Collection, data.Query, data.Projection)
	if err != nil {
		log(1, err.Error())
		job.SendWarning([]byte("\"error\":\"" + err.Error() + "\""))
	}
	err = job.Err()
	return response, err
}
