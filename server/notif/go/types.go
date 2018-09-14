package main
import (
	"log"
	"fmt"
	"bytes"
	"time"
)

type UAction struct{
	Record Record
	Goal Goal
	Rules Rec2Notif
}

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
		Title : "Test Goal",
	}
	return goal
}

type Goal struct{
	Title string
	Id string`json:_id`
	Desc string
	Done bool
}
func (u Goal)String() string{
	return "<"+u.Title+ " goal@ "+ u.Id +">"
}

type Record struct{
	Command string
	Type string
	Content map[string]string
	Id string`json:_id`
	Date time.Time
	UserId string
}
func createKeyValuePairs(m map[string]string) string {
	b := new(bytes.Buffer)
	for key, value := range m {
		fmt.Fprintf(b, "%s=\"%s\"\n", key, value)
	}
	return b.String()
}
func (u Record)String() string{
	return "<record "+u.Command+" //"+u.Id+u.Command+" content:\n"+
	createKeyValuePairs(u.Content)+">"
}

type Notification struct{
	Medium string
	Time time.Time
	// this string is used to create a (Notif,Goal)->notif
	ResolveRules string
	Content map[string]string
	AppId string
	Id string
	UserId string
}
func (u Notification)String() string{
	const layout = "Jan 2, 18:45"
	return "<"+u.Medium+" notif"+u.Content["Type"]+" @ " +
	u.Time.Format(layout) +">"
}
