package main

import (
	"./adder"
	"fmt"
)

func main() {
	fmt.Println("Starting dbtools Gearman workers.")
	err := adder.Create()
	if err != nil {
		fmt.Println("Could not create Adder worker: ")
		fmt.Println(err)
	}
}
