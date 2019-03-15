package main

import (
	"log"
)

func main() {
	log.Println("starting")
	link_g := Link{
		Ref : "1233",
		Target : "goal",
	}
	link_m := Link{
		Ref : "123",
		Target : "Mapper",
	}
	rec := Record{
		Name : "A record about blah",
		Type : "Web page",
	}
	g, mapper := Get_Goal_Mapper(link_g,link_m)
	log.Println("goal",g )
	notif := mapper.Apply(rec,g)

	log.Println("notif",notif)
}

