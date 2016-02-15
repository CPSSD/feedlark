package adder

import (
	"fmt"
	"github.com/mikespook/gearman-go/worker"
	//	"gopkg.in/mgo.v2"
)

func Create() error {
	fmt.Println("Creating Gearman worker 'db-add'")
	w := worker.New(worker.OneByOne)
	w.ErrorHandler = func(e error) {
		fmt.Println(e)
	}
	w.AddServer("tcp4", "127.0.0.1:4730")
	w.AddFunc("db-add", DbAdd, worker.Unlimited)

	if err := w.Ready(); err != nil {
		fmt.Println("Fatal error")
		fmt.Println(err)
		return err
	}
	go w.Work()
	return nil
}

func DbAdd(job worker.Job) ([]byte, error) {
	fmt.Println("database adder called!")
	return nil, nil
}
