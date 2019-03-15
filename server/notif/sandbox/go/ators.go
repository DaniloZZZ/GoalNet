package main
import (
	"log"
)

func Get_Goal_Mapper (l_goal Link, l_mapper Link) (Goal, Rec2Notif) {
	log.Println("Getting goal and mapper from lnks")
	g := Goal{ }
	g = g.Load(l_goal)
	mapp := Rec2Notif { }
	mapp = mapp.Load(l_mapper)
	return g, mapp
}

