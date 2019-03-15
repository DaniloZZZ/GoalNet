package main
import (
	"log" 
	"time"
)

type Link struct{
	Ref string
	Target string
}
func (u Link)String() string{
	return u.Target + " @ "+ u.Ref
}

type Rec2Notif struct{
	Apply func(Record,Goal) Notification
}

type Getter struct{
	From string
	To string
}
func (s Getter)Apply( i Link) Goal{
	log.Println("Here we pretend some api call")
	goal := Goal{
		Id : "1231",
		Name : "Test Goal",
	}
	return goal
}

type Goal struct{
	Name string
	Id string
}
func (u Goal)String() string{
	return "<"+u.Name+ " goal@ "+ u.Id +">"
}

type Record struct{
	Name string
	Type string
	Id string
}

type Notification struct{
	Medium string
	Time time.Time
	Id string
}
func (u Notification)String() string{
	const layout = "Jan 2, 18:45"
	return "<"+u.Medium+" notif @ " +
	u.Time.Format(layout) +">"
}


