package main
import (
	"log"
	"net/http"
	"github.com/jcuga/golongpoll"
)


func ValidateApiKey(api string, cat string)bool{
	log.Print("validating",api,cat)
	return true
}


func getSubscriptionProvider( manager *golongpoll.LongpollManager) func (w http.ResponseWriter, r *http.Request){
	return func(w http.ResponseWriter, r *http.Request){
		category := r.URL.Query().Get("category")
		apikey:= r.URL.Query().Get("apikey")
		//message := r.URL.Query().Get("message")

		w.Header().Set("Access-Control-Allow-Origin", "*")
		if ValidateApiKey(apikey,category){
			manager.SubscriptionHandler(w, r)
		}else{
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Wrong api key"))
			return
		}
	}
}
