package main

import (
	"./adder"
	"./getter"
	"fmt"
)

func main() {
	fmt.Println("Starting dbtools Gearman workers.")
	go adder.Create()
	go getter.Create()
	err := adder.Create()
	if err != nil {
		fmt.Println("Could not create Adder worker: ")
		fmt.Println(err)
	}
	err = getter.Create()
	if err != nil {
		fmt.Println("Could not create Getter worker: ")
		fmt.Println(err)
	}
}
