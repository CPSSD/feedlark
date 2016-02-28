package main

import (
	"./adder"
	"./getter"
	"fmt"
)

func main() {
	fmt.Println("Starting dbtools Gearman workers.")
	go adder.Create()
	getter.Create()
}
