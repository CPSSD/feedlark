package dbhelp

import (
	"fmt"
	"os"
	"time"

	"gopkg.in/mgo.v2"
)

func GetURL() string {
	return "127.0.0.1:9001"
}

func Log(level int, s string) {
	//level 0 = INFO
	//level 1 = WARNING
	//level 2 = ERROR
	now := time.Now().Format("15:04:05 02/01/2006")

	levels := []string{"INFO", "WARNING", "ERROR"}
	fmt.Printf("%s %s: %s\n", now, levels[level], s)
}

func CorrectKey(key string) bool {
	envKey := os.Getenv("SECRETKEY")
	Log(0, "Checking secret key")
	if envKey == "" || envKey == key {
		return true
	}
	return false
}

func CreateSession(url string, database string, collection string) *mgo.Collection {
	session, err := mgo.Dial(url)
	if err != nil {
		Log(2, err.Error())
		panic(err.Error())
	}

	if os.Getenv("ENVIRONMENT") == "PRODUCTION" {
		session.DB(database).Login("feedlark", "hackmeplz")
	}

	return session.DB(database).C(collection)
}
