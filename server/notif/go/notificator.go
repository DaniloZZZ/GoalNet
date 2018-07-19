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
// conditions e.g time or _external_ http rnesource
// a notification and it's resolver is stored.
//
type NotificationIntent struct{
	Notif Notification
	Resolve func(notif Notification)bool
}

var storage map[string]NotificationIntent
// This functions saves a NotificationIntent depending on
// goal's settings 
func ScheduleNotification(
	notif Notification, g Goal){
		log.Print("Scheduling",notif)
		id := g.Id + notif.Id
		new_intent := NotificationIntent{
			Notif : notif,
			Resolve : func(notif Notification) bool{
				log.Print("Resolving",notif)
				return true
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
	go func(){
		for{
			time.Sleep(500)
			for id := range storage{
				intent := storage[id]
				if intent.Resolve(intent.Notif){
					// Send the notification
					n := intent.Notif
					log.Print("sending",n)
					manager.Publish(
						n.Medium +":"+ n.AppId ,
						n.Content,
					)
					delete(storage,id)
				}
			}
		}
	}()

	// Serve our event subscription web handler
	http.HandleFunc("/user/events", getSubscriptionProvider(manager))
	log.Print("Serving longpoll webpage at http://127.0.0.1:"+port)
	http.ListenAndServe("127.0.0.1:"+port, nil)

	manager.Shutdown() // Stops the internal goroutine that provides subscription behavior
	// Serve event emitter web handler
	//http.HandleFunc("/emit",getEmittedEventHandler(manager))
	//sender := getEmittedEventHandler(manager)
}

