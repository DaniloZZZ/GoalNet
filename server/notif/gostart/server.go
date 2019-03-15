package main
import (
	"fmt"
	"log"
	"net/http"
	"os/signal"
	"os"
	"syscall"
	//m "math"
)
type callback struct{
	port,y int
	ref *int
}

func (p callback) ServeHTTP(w http.ResponseWriter, r *http.Request){
	w.Write( []byte( fmt.Sprintf("Hello, welcome to the port %v",p.port)))
	w.Write( []byte( fmt.Sprintf("The value is %v",*p.ref)))
}

func main(){
	port:=3200
	fmt.Println("starting server")
	var p int
	p =10
	go func(){
		err:=http.ListenAndServe(":3200",callback{port,10,&p})
		fmt.Println("Error!")
		fmt.Println(err)
	}()
	p=3
	trig:=false
	for {
		if trig{
			p++
			if p>10003{
				trig=false}
		} else{
			p--
			if p<3{
				trig=true}
		}
	}

	waitForSignal()
}

func waitForSignal() {
	ch := make(chan os.Signal)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	s := <-ch
	log.Printf("Got signal: %v, exiting.", s)
}
