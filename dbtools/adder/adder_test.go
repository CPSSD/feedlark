package adder

import (
	"fmt"
	"gopkg.in/mgo.v2/bson"
	//"strconv"
	"testing"
)

func TestDocumentAdd(t *testing.T) {
	_, err := AddDocument("127.0.0.1:27017", "testing", "adder", bson.M{"info": "nothing worth saying"})
	if err != nil {
		t.Error(err)
	}
}

func TestDocumentUpdate(t *testing.T) {
	id := bson.NewObjectId()
	_, err := AddDocument("127.0.0.1:27017", "testing", "updater", bson.M{"_id": id, "memes": "are great"})
	if err != nil {
		t.Error(err)
	}
	_, err = UpdateDocument("127.0.0.1:27017", "testing", "updater", bson.M{"selector": bson.M{"_id": id}, "updates": bson.M{"memes": "are ok"}})
	if err != nil {
		t.Error(err)
	}
}

func TestNewDocumentUpsert(t *testing.T) {
	rawResult, err := UpsertDocument("127.0.0.1:27017", "testing", "upserter", bson.M{"selector": bson.M{"memes": "are not ok"}, "updates": bson.M{"memes": "are ok"}})
	if err != nil {
		t.Error(err)
	}
	var result struct {
		Status string
		NewDoc bool `bson:"new_doc"`
	}
	bson.Unmarshal(rawResult, &result)
	if result.Status != "ok" {
		fmt.Println("Status != ok")
		t.FailNow()
	}
	if !result.NewDoc {
		fmt.Println("Is updating old doc, should be new doc")
		t.FailNow()
	}
}

func TestExistingDocumentUpsert(t *testing.T) {
	AddDocument("127.0.0.1:27017", "testing", "upserter", bson.M{"love": "memes"})
	rawResult, err := UpsertDocument("127.0.0.1:27017", "testing", "upserter", bson.M{"selector": bson.M{"love": "memes"}, "updates": bson.M{"love": "dank memes"}})
	if err != nil {
		t.Error(err)
	}
	var result struct {
		Status string
		NewDoc bool `bson:"new_doc"`
	}
	bson.Unmarshal(rawResult, &result)
	if result.Status != "ok" {
		fmt.Println("Status != ok")
		t.FailNow()
	}
	if result.NewDoc {
		fmt.Println("Is new doc, should be old")
		t.FailNow()
	}
}
