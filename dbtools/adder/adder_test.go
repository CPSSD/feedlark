package adder

import (
	"gopkg.in/mgo.v2/bson"
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
