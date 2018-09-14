package main
import (
	"log"
	"encoding/json"
)
type ActionRequest struct{
	Record Record
	Goal Goal
}

func Parse_Action(data string) (
	Record,Goal,Rec2Notif) {
	// Parse data from POST http request to 
	// Action object. Acceptable format:
	// {"Goal":<Goal json>,
	//	"Record":<Record json>}
	log.Print("Request body",data)
	var Ar ActionRequest
	json.Unmarshal([]byte(data), &Ar)
	log.Print("Parsed Action",Ar.Record,Ar.Goal)
	var r Record
	var g Goal
	if Ar.Goal.Title==""{
		log.Print("No title for goal provided, fetching from DB")
		l := Link{ Ref:g.Id }
		g.Load(l)
	} else { g= Ar.Goal }
	r = Ar.Record
	var rn Rec2Notif
	//r.Load(l)
	l := Link{ Ref:"42" }

	return r,g,rn.Load(l)
}
func fetchRec2N(rec Record)(Goal,Rec2Notif) {
	var g Goal
	l := Link{ Ref:g.Id }
	g.Load(l)
	var rn Rec2Notif
	//r.Load(l)
	l = Link{ Ref:"42" }

	return g,rn.Load(l)
}
