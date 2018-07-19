package main
import (
	"fmt"
	"log"
	"net/http"
	"os/signal"
	"os"
	"syscall"
	"io/ioutil"
	//m "math"
)
type callback struct{
	port,y string
	ref *int
}

func (p callback) ServeHTTP(w http.ResponseWriter, r *http.Request){
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body",
		http.StatusInternalServerError)
	}
	rec,goal,rec2notif := Parse_Action(string(body))
	rec.Save()
	notif := rec2notif.Apply(rec,goal)
	ScheduleNotification(notif,goal)

	resp :=  fmt.Sprintf("Hello, welcome to the port %v",p.port)
	log.Print("respoding",resp)
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.WriteHeader(http.StatusOK)
	w.Write( []byte(resp))
	return
}

func main(){
	clb := callback{
		port : "3200",
	}
	log.Print("Starting record server on port ",clb.port)
	go func(){
		err := http.ListenAndServe(
			":"+clb.port,clb)
		if err!=nil{
			fmt.Println("Error!")
			fmt.Println(err)
		}
	}()
	StartNotificator()
	waitForSignal()
}

func waitForSignal() {
	ch := make(chan os.Signal)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	s := <-ch
	log.Printf("Got signal: %v.\nBye.", s)
}
