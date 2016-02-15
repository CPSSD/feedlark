package main

import (
	"fmt"
	"github.com/mikespook/gearman-go/worker"
	//	"gopkg.in/mgo.v2"
)

func main() {
	w := worker.New(worker.OneByOne)
	defer w.Close()
	w.ErrorHandler = func(e error) {
		fmt.Println(e)
	}
	w.AddServer("tcp4", "127.0.0.1:4730")
	w.AddFunc("db-add", DbAdd, worker.Unlimited)
	if err := w.Ready(); err != nil {
		fmt.Println("Fatal error")
		fmt.Println(err)
		return
	}
	go w.Work()
}

func DbAdd(job worker.Job) ([]byte, error) {
	fmt.Println("database adder called!")
	return nil, nil
}
