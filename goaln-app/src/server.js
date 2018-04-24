var express = require('express');
var Goal = require('./db/Shemas.js').Goal;
var User = require('./db/Shemas.js').User;

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

function find_user(id){
	console.log('getting user num',id)
	return new Promise((resolve,reject)=>{
		User.findOne(
			{
				_id :id
			}
			,function(e,g){
				resolve(g)
				if (e) reject(e)
			})
	})
}

function get_users(){
	console.log('getting users')
	return new Promise((resolve,reject)=>{
		User.find(
				{}
			,function(e,g){
				resolve(g)
				if (e) reject(e)
			})
	})
}
function find_goals(ids){
	console.log('getting goal num',ids)
	return new Promise((resolve,reject)=>{
		Goal.find(
				{
					_id : {$in: ids}
				},
				function(e,g){
					if(e) reject(e)
					resolve(g)
				})
	})
}
app.get('/usergoals', function (req, res) {
		var u_id = req.query.id;
		//res.header("Access-Control-Allow-Origin", "*");
		//res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
		find_user(u_id).then((u)=>{
			console.log('got user',u)
			console.log('got name',u.fname)
			return find_goals(u.goal_ids)
		}).then((gs)=>{
			console.log('got goals',gs)
			res.send(gs)
		})
});

app.get('/user', function (req, res) {
		var id = req.query.id;
		find_user(id).then(us=>{res.send(us)}).catch(res.send)
});

app.get('/users', function (req, res) {
		var id = req.query.id;
		get_users().then(us=>{res.send(us)}).catch(res.send)
});

app.get('/goals', function (req, res) {
		var id = req.query.id;
});

app.post('/newgoal', cors(),function(req, res) {
	  res.header("Access-Control-Allow-Origin", "*");
	    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
	    res.header("Access-Control-Allow-Methods", "GET, POST");
	    var name = req.body.name
		g =req.body
		goal = new Goal({
			title:g.title,
			desc:g.desc,
			deadline:g.date,
		})
		goal.save().then((ng)=>{
			User.update(
					{_id:g.id},
					{ $push:{goal_ids:ng._id} },
					console.log
					)
			console.log(ng);
			res.send("OK")})
});

app.post('/donegoal', cors(),function(req, res) {
	var id = req.query.id;
	Goal.update(
		{_id:id},
		{$set:{done:true} },
		console.log
	)
	res.send("OK")
});
mongoose.connect('mongodb://localhost/local');
app.listen(3030, function () {
	  console.log('Example app listening on port 3000!');
});
