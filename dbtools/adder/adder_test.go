package adder

import (
	"testing"
)

func TestCreate(t *testing.T) {
	err := Create()
	if err != nil {
		t.Error(err)
	}
}

func TestDocumentAdd(t *testing.T) {
	err := AddDocument("127.0.0.1:27017", "testing", "adder", "{\"data\":\"nothing worth saying\"}")
	if err != nil {
		t.Error(err)
	}
}

func TestDocumentUpdate(t *testing.T) {
	err := AddDocument("127.0.0.1:27017", "testing", "updater", "{\"_id\":ObjectId(000000000000),\"dank\":\"memes\"}")
	if err != nil {
		t.Error(err)
	}
	err = UpdateDocument("127.0.0.1:27017", "testing", "updater", "{\"id\":ObjectId(000000000000), \"updates\":{\"dank\":\"fruits\"}}")
	if err != nil {
		t.Error(err)
	}
}
