package main

import (
	"log"
	"time"
)
type DB interface{
	Load(Link)
	Save(Link)
}
func (me Goal) Load( l Link) Goal{
	log.Println("Loading goal")
	me.Name = "A goal just from db"
	me.Id = l.Ref
	return me
}
func (me Rec2Notif) Load(l Link) Rec2Notif{
	log.Println("Loading rec2notif")
	tim := time.Now()
	app := func (rec Record,g Goal) (
		Notification) {
			log.Println("Mapper hello")
			n := Notification{
				Medium : "telegram",
				Time : tim,
				Id : "1231",
			}
			return n
		}
	me.Apply = app
	return me
}

func Generate_Notification_generator (record Record, goal Goal) (Goal, Notification) {
	log.Println("Now generating map from record to notif")
	return Goal{},Notification{}

}


