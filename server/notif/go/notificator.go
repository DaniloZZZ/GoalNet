package main
import (
	"log"
	//"hash"
	"time"
	"net/http"
	"github.com/jcuga/golongpoll"
)

//
// In order to send notification only at given 
// conditions e.g time or _external_ http resource
// a notification and it's resolver is stored.
//
type NotificationIntent struct{
	Notif Notification
	Goal Goal
	Resolve func() (bool)
	NextNotif func(Notification) (Notification,bool)
}
var CheckDelay=2000

var storage map[string]NotificationIntent
// This functions saves a NotificationIntent depending on
// goal's settings 
func ScheduleNotification(
	notif Notification, g Goal){
		log.Print("Scheduling",notif)
		id := g.Id + notif.Id
		new_intent := NotificationIntent{
			Notif : notif,
			Goal : g,
			Resolve : func() (bool){
				dosend:=false
				if notif.ResolveRules=="at"{
					diff:=time.Since(notif.Time).Seconds()
					log.Print("diff is",diff)
					if diff>-float64(CheckDelay)/1000.{
						dosend=true
					}
				}

				log.Print("Resolving",notif)
				return dosend
			},
			NextNotif : func(Notification) (Notification,bool){
				schedule_next:=false
				next := Notification{}
				return next , schedule_next
			},
		}
		// Saving the intent to storage. 
		// Goroutine will check it then and send if 
		// Resolver returnes true
		storage[id] = new_intent
	}

func StartNotificator(){
	port := "3100"
	storage = make(map[string]NotificationIntent)

	manager, err := golongpoll.StartLongpoll(
		golongpoll.Options{
		LoggingEnabled: true,
	})
	if err != nil {
		log.Fatalf("Failed to create manager: %q", err)
	}

	// Serve debug webpage
	//http.HandleFunc("/debug",DebugPage)
	log.Print("starting loop checking")
	step:=func(){

		for id := range storage{
			intent := storage[id]
			dosend:=intent.Resolve()
			if dosend{
				// Send the notification to all who
				// subscribed to "Medium:AppId" category
				n := intent.Notif
				log.Print("sending",n)
				manager.Publish(
					n.Medium +":"+ n.AppId ,
					n.Content,
				)
				delete(storage,id)
				next_notif, schedule_next :=
				intent.NextNotif(intent.Notif)
				if schedule_next{
					ScheduleNotification(next_notif,intent.Goal)
				}
			}
		}
	}
	go func(){
		for{
			time.Sleep(time.Duration(CheckDelay)*time.Millisecond)
			step()
		}
	}()
	// Serve our event subscription web handler
	notif_endpoint := "/events"
	http.HandleFunc(notif_endpoint, getSubscriptionProvider(manager))
	log.Print("Serving longpoll webpage at http://127.0.0.1:"+port+notif_endpoint)
	http.ListenAndServe(":"+port, nil)

	manager.Shutdown() // Stops the internal goroutine that provides subscription behavior
	// Serve event emitter web handler
	//http.HandleFunc("/emit",getEmittedEventHandler(manager))
	//sender := getEmittedEventHandler(manager)
}

