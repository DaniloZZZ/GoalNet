package main

import (
	"log"
)
type ActionRequest struct{
	Record  string
}

func Parse_Action(data string) (
	Record,Goal,Rec2Notif){
	log.Print("data from req",data)

	var r Record
	var g Goal
	var rn Rec2Notif
	l := Link{
		Ref:"121",
	}
	r.Load(l)
	r.Name = data
	return r,g.Load(l),rn.Load(l)
}
