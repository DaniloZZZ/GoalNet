var express = require('express');
var Goal = require('./db/Shemas.js').Goal;
var User = require('./db/Shemas.js').User;
var config = require('./config.js')


var mongoose = require('mongoose')
var cors= require('cors')

var app = express();
app.use(function(req, res, next) {
	res.header("Access-Control-Allow-Origin", "*");
	res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
	res.header("Access-Control-Allow-Methods", "POST, GET");
	next();
});
app.use(express.json());       // to support JSON-encoded bodies
app.use(express.urlencoded()); // to support URL-encoded bodies

app.get('/', function (req, res) {
	  res.send('Hello World!');
});


app.get('/long', function (req, res) {
	console.log('got req')
	var val = req.query.val;
	var sl = new Promise((resolve,rej)=>{
		response=res
		console.log('got param',val)
		setTimeout(()=>{
			response.send('ok from server')
			resolve(res)
		},parseInt(val))
	})
	sl.then(res=>console.log('sent'))
});

console.log(config.db)
var port = 3030;
app.listen(port, function () {
	  console.log('Longpoll test app listening on port '+port+'!');
});
