package main

import (
	"log"
	"time"
	"bytes"
	"io/ioutil"
	"encoding/json"
	"net/http"
	"net/url"
)
type DB interface{
	Load(Link)
	Save(Link)
}
var server_endpoint="http://localhost:3030"
func (me Goal) Load( l Link) Goal{
	log.Println("Loading goal from db by id",l.Ref)
	me.Title= "A goal just from db"
	me.Id = l.Ref
	return me
}
func (me Goal) Save ()bool{
	log.Println("Saving goal",me)
	return true
}
func (me Rec2Notif) Load(l Link) Rec2Notif{
	// In futyure, you can load custom rec2notif 
	// depending on link ref provided in POST req
	log.Println("Loading rec2notif")
	tim := time.Now().Add(3*time.Second)
	id := "5adcefbaed9d970d42d33d65"
	apply := func (rec Record,g Goal) Notification {
			log.Println("Mapper hello")
			log.Println("record content.type",rec.Content["type"])
			log.Println("record name",rec.Command)
			if rec.Command=="Pomodoro_Start"{
				status := Get_Pomodoro_User(id)
				log.Print("----\nSTATUS\n",status)
				n := Notification{
					Medium : "telegram",
					Content : map[string]string{
						"Type":"Pomodoro_Relax",
						"GoalName":g.Title,
					},
					ResolveRules: "at",
					Time : time.Now().Add(10*time.Second),
					AppId : "0",
					Id : "1231",
				}
			return n
			}else {
				n := Notification{
					Medium : "telegram",
					Content : map[string]string{
						"Type":"Pomodoro_Stop",
						"GoalName":g.Title,
					},
					ResolveRules: "at",
					Time : tim,
					AppId : "0",
					Id : "1231",
				}
			return n
			}
		}
	me.Apply = apply
	return me
}
func (me Rec2Notif) Save ()bool{
	log.Println("Saving rec2notif",me)
	return true
}

func (me Record) Load (Link) Record{
	r := Record{
		Type : "Telegram",
		Command : "some record",
		Id : "123123",
	}
	return r
}
type PostRecord struct{
	Id string `json:"id"`
	Props Record `json:"props"`
	Parent map[string]string `json:"parent"`
}

func (me Record) Save ()bool{
	log.Println("Saving record",me)
	me.Date=time.Now()
	me.UserId = "5adcefbaed9d970d42d33d65"
	record:=map[string]interface{}{
		"id":me.Id,
		"parent":map[string]string{
			"kind":"User",
			"id":me.UserId,
		},
		"props":map[string]interface{}{
			"type":me.Type,
			"command":me.Command,
			"content":me.Content,
			"date":me.Date,
		},
	}
	json,err:= json.Marshal(record)
	if err!=nil{
		log.Print("!!\nALARM\n",err)
	}
	log.Println("**\n**\n -->>")
	log.Println(string(json))
	resp, err:= http.Post(
		server_endpoint+"/record",
		"application/json",
		bytes.NewBuffer(json),
	)
	log.Println(resp)
	if err==nil{
		return true
	} else{
		log.Println(err)
		return false
	}
}

func Get_Pomodoro_User(id string) string{
	filter,_ := json.Marshal(map[string]string{
			"type":"pomodoro",
		})

	q:=url.Values{}
	q.Add("id",id)
	q.Add("filter",string(filter))
	resp, err:= http.Get(
		server_endpoint+"/user/records?"+q.Encode(),
	)
	if err!=nil{
		log.Panic(err)
		return "error"
	}else{
		body, _:= ioutil.ReadAll(resp.Body)
		log.Println("GOT\n<<--\n",string(body))
		var list [3]Record
		json.Unmarshal(body, &list)
		Comm := list [0].Command
		log.Println("COMM\n",Comm)
		if Comm=="Pomodoro_Start"{
			return "work"
		}else if Comm=="Pomodoro_Done"{
			return "relax"
		}else{
			return "no"
		}
	}
}

func Generate_Notification_generator (record Record, goal Goal) (Goal, Notification) {
	log.Println("Now generating map from record to notif")
	return Goal{},Notification{}

}


