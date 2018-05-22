logger = require 'log4js'
log = logger.getLogger('api-baseNode')
log.level='debug'

config = require './config-server.js'
mongoose = require('mongoose')
express = require('express')
#Schemas= require '../DB/schema/Shemas.js'
Goal = require './db/GoalNode.coffee'

cors = require('cors')
app = express()

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

new Goal(app).registerAppEndpoints()

"""
app.get '/gddoal', (req, res) ->
	log.info req.url, 'got connection ',req.headers.host
	log.debug req.headers
	id = req.query.id
	log.debug id
	Goal.find
		_id:req.query.id
		(err,goal)->
			if err
				log.error err.name, err.message
				res.status 400
				res.send err.name
			else
				log.info 'db returned: ',goal
				res.send goal

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
		sched: g.sched
	})
	console.log g
	goal.save().then (ng) ->
		User.update { _id: g.id }, { $push: goal_ids: ng._id }, console.log
		console.log ng
		res.send 'OK'
		return
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
"""

console.log config.db
mongoose.connect config.db
port = 3030
app.listen port, ->
	console.log 'Example app listening on port ' + port + '!'
	return
