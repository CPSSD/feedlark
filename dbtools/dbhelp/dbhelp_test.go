package dbhelp

import (
	"testing"
)

func TestGetURL(t *testing.T) {
	if GetURL() != "127.0.0.1:9001" {
		t.Error("Failed to pass TestGetURL")
	}
}

func TestCreateSession(t *testing.T) {
	// Note that if if GetSession error it panics which will error here also.
	coll := CreateSession(GetURL(), "feedlark", "g2g")
	if coll == nil {
		t.Error("Failed to pass TestCreateSession")
	}
}
