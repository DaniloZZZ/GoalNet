package main
import (
	"fmt"
	"log"
	"net/http"

	"github.com/jcuga/golongpoll"
)

func main() {
	manager, err := golongpoll.StartLongpoll(golongpoll.Options{
		LoggingEnabled: true,
		// NOTE: if not defined here, other options have reasonable defaults,
		// so no need specifying options you don't care about
	})
	if err != nil {
		log.Fatalf("Failed to create manager: %q", err)
	}
	// Serve debug webpage
	http.HandleFunc("/debug",DebugPage)

	// Serve our event subscription web handler
	http.HandleFunc("/user/events", getSubscriptionProvider(manager))

	// Serve event emitter web handler
	http.HandleFunc("/emit",getEmittedEventHandler(manager))

	fmt.Println("Serving debug webpage at http://127.0.0.1:8081/debug")
	http.ListenAndServe("127.0.0.1:8081", nil)

	// We'll never get here as long as http.ListenAndServe starts successfully
	// because it runs until you kill the program (like pressing Control-C)
	// Buf if you make a stoppable http server, or want to shut down the
	// internal longpoll manager for other reasons, you can do so via
	// Shutdown:
	manager.Shutdown() // Stops the internal goroutine that provides subscription behavior
	// Again, calling shutdown is a bit silly here since the goroutines will
	// exit on main() exit.  But I wanted to show you that it is possible.
}
func ValidateApiKey(apikey,user,action string)(bool){
	if apikey=="DEBUG42"{
		return true
	}else{
		return false
	}
}
func getSubscriptionProvider( manager *golongpoll.LongpollManager) func (w http.ResponseWriter, r *http.Request){
	return func(w http.ResponseWriter, r *http.Request){
		user := r.URL.Query().Get("user")
		action := r.URL.Query().Get("action")
		apikey:= r.URL.Query().Get("apikey")
		//message := r.URL.Query().Get("message")

		//ok :=ValidateApiKey(apikey,user,action)
		if ValidateApiKey(apikey,user,action){
			manager.SubscriptionHandler(w, r)
		}else{
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Wrong api key"))
			return
		}
	}
}

func getEmittedEventHandler( manager *golongpoll.LongpollManager) func (w http.ResponseWriter, r *http.Request){
	// Return the handler function
	return func(w http.ResponseWriter, r *http.Request){
		log.Println("got this query:")
		log.Println(r.URL.Query())

		user := r.URL.Query().Get("user")
		action := r.URL.Query().Get("action")
		apikey := r.URL.Query().Get("apikey")
		//message := r.URL.Query().Get("message")

		// Perform validation on url query params:
		//ok :=ValidateApiKey(apikey,user,action)
		if ValidateApiKey(apikey,user,action){
			// Publish to debug
			manager.Publish("debug",r.URL.Query())
			// Notify the subscribed users
			// manager.Publish(action,r.Url.Query())
		} else{
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Wrong api key"))
			return
		}

	}
}

func DebugPage(w http.ResponseWriter, r *http.Request){
	fmt.Fprintf(w, `
<html>
<head>
    <title>debug notificator for goalnet</title>
</head>
<body>
    <h1>GoalNet Notifications</h1>
    <ul id="notifications"></ul>
<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
<script>

    // for browsers that don't have console
    if(typeof window.console == 'undefined') { window.console = {log: function (msg) {} }; }

    // Start checking for any events that occurred after page load time (right now)
    // Notice how we use .getTime() to have num milliseconds since epoch in UTC
    // This is the time format the longpoll server uses.
    var sinceTime = (new Date(Date.now())).getTime();

    var category = "debug";

    (function poll() {
        var timeout = 20;  // in seconds
        var optionalSince = "";
        var apikey = "DEBUG42";
        if (sinceTime) {
            optionalSince = "&since_time=" + sinceTime;
        }
        var pollUrl = "/user/events?timeout=" + timeout + "&category=" + category + optionalSince +"&apikey="+apikey;
        // how long to wait before starting next longpoll request in each case:
        var successDelay = 10;  // 10 ms
        var errorDelay = 5000;  // 3 sec
        $.ajax({ url: pollUrl,
            success: function(data) {
                if (data && data.events && data.events.length > 0) {
                    // got events, process them
                    // NOTE: these events are in chronological order (oldest first)
                    for (var i = 0; i < data.events.length; i++) {
                        // Display event
                        var event = data.events[i];
                        $("#notifications").append("<li>" +JSON.stringify(event.data) + " at " + (new Date(event.timestamp).toLocaleTimeString()) +  "</li>")
                        // Update sinceTime to only request events that occurred after this one.
                        sinceTime = event.timestamp;
                    }
                    // success!  start next longpoll
                    setTimeout(poll, successDelay);
                    return;
                }
                if (data && data.timeout) {
                    console.log("No events, checking again.");
                    // no events within timeout window, start another longpoll:
                    setTimeout(poll, successDelay);
                    return;
                }
                if (data && data.error) {
                    console.log("Error response: " + data.error);
                    console.log("Trying again in "+errorDelay+" seconds...")
                    setTimeout(poll, errorDelay);
                    return;
                }
                // We should have gotten one of the above 3 cases:
                // either nonempty event data, a timeout, or an error.
                console.log("Didn't get expected event data, try again shortly...");
                setTimeout(poll, errorDelay);
            }, dataType: "json",
        error: function (data) {
            console.log("Error in ajax request--trying again in #{errorDelay} seconds...");
            setTimeout(poll, errorDelay);  // 3s
        }
        });
    })();
</script>
</body>
</html>`)
}

