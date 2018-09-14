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
var CheckDelay=1000

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
			NextNotif : func(prev_notif Notification) (Notification,bool){

				id := "5adcefbaed9d970d42d33d65"
				status:=Get_Pomodoro_User(id)
				log.Print("\n---STATUS\n",status)
				var command string
				schedule_next:=true
				if status=="work"{
					command="Pomodoro_End"
				}else if status =="relax"{
					command="Pomodoro_Start"
				}else{
					schedule_next = false
				}
				if schedule_next{

					rec:=Record{
						Command : command,
						Type : "pomodoro",
						UserId : notif.UserId, // Preserve uid
						// in chained notifications
					}
					goal,rec2notif := fetchRec2N(rec)
					//These are programmatically emitted recors
					// Probably should configure if saving
					rec.Save()
					next_notif := rec2notif.Apply(rec,goal)
					return next_notif , schedule_next
				}else{
					return Notification{},false
				}

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
				log.Print("==>>\nsending notification",n)
				manager.Publish(
					n.Medium +":"+ n.AppId ,
					n.Content,
				)
				delete(storage,id)
				next_notif, schedule_next :=
				intent.NextNotif(intent.Notif)
				if schedule_next{
					log.Println("\n **NewNotif**\n",next_notif)
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

