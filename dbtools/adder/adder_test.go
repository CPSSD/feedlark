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
