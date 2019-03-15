var express =require("express")
var cors = require('cors')
var fs=require("fs")

var app = express()

app.use(express.static(__dirname ));
app.use(cors)

app.get('/', function(req,res){
	
	res.sendFile('./index.html')
}
);

app.get('/main.js', function(req,res){
	
	res.sendFile('./main.js')
}
);
var port = 3111
app.listen(port)
console.log("app is on port ",port)
