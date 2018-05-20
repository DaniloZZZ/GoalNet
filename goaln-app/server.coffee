express = require('express')
Goal = require('./db/Shemas.js').Goal
User = require('./db/Shemas.js').User
config = require './config-server.js'
mongoose = require('mongoose')
cors = require('cors')
app = express()

find_user = (id) ->
	console.log 'getting user num', id
	new Promise((resolve, reject) ->
		User.findOne { _id: id }, (e, g) ->
			resolve g
			if e
				reject e
	)

get_users = ->
	console.log 'getting users'
	new Promise((resolve, reject) ->
		User.find {}, (e, g) ->
			resolve g
			if e
				reject e
			return
		return
		)

find_goals = (ids) ->
	console.log 'getting goal num', ids
	new Promise((resolve, reject) ->
		Goal.find { _id: $in: ids }, (e, g) ->
			if e
				reject e
			resolve g
			return
		return
		)

app.use (req, res, next) ->
	res.header 'Access-Control-Allow-Origin', '*'
	res.header 'Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept'
	res.header 'Access-Control-Allow-Methods', 'POST, GET'
	next()
	return
app.use express.json()
# to support JSON-encoded bodies
app.use express.urlencoded()
# to support URL-encoded bodies
app.get '/', (req, res) ->
	res.send 'Hello World!'
	return
value = null
response = null
app.get '/setlong', (reqweb, resweb) ->
	valweb = reqweb.query.val
	console.log 'got setlong'
	if response
		response.send valweb
		response = null
		resweb.send value
	else
		resweb.send 'NOthing'
	return
app.get '/long', (req, res) ->
	console.log 'got req'
	val = req.query.val
	response = res
	value = val
	setTimeout (->
		if response
			response.send 'delay'
			response = null
			return
		), 6000
	return
app.get '/usergoals', (req, res) ->
	u_id = req.query.id
	#res.header("Access-Control-Allow-Origin", "*");
	#res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
	find_user(u_id)
	.then((u) ->
		console.log 'got user', u
		console.log 'got name', u.fname
		find_goals u.goal_ids
	).then (gs) ->
		console.log 'got goals', gs
		res.send gs
app.get '/user', (req, res) ->
	id = req.query.id
	find_user(id).then((us) ->
		res.send us
		return
	).catch res.send
	return
app.get '/users', (req, res) ->
	id = req.query.id
	get_users().then((us) ->
		res.send us
		return
	).catch res.send
	return
app.get '/goals', (req, res) ->
	id = req.query.id
	return
app.post '/newgoal', cors(), (req, res) ->
	res.header 'Access-Control-Allow-Origin', '*'
	res.header 'Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept'
	res.header 'Access-Control-Allow-Methods', 'GET, POST'
	name = req.body.name
	g = req.body
	goal = new Goal({
		title: g.title,
		desc: g.desc,
		deadline: g.date
	})
	goal.save().then (ng) ->
		User.update { _id: g.id }, { $push: goal_ids: ng._id }, console.log
		console.log ng
		res.send 'OK'
		return
	return
app.post '/comment', cors(), (req, res) ->
	id = req.query.id
	d = req.body
	console.log 'new comment', d
	if d.act == 'add'
		Goal.update { _id: d.id }, { $push: comments:
			user_id: d.uid
			text: d.text
			date: d.date }, console.log
		res.send 'OK'
	return
app.post '/donegoal', cors(), (req, res) ->
	id = req.query.id
	Goal.update _id:id, $set:done:true, console.log
	res.send 'OK'
	return
app.post '/donegoal', cors(), (req, res) ->
	id = req.query.id
	Goal.update _id:id, $set: done: true, console.log
	res.send 'OK'
	return
console.log config.db
mongoose.connect config.db
port = 3030
app.listen port, ->
	console.log 'Example app listening on port ' + port + '!'
	return
