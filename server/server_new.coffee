
config = require './config-server.js'
mongoose = require('mongoose')
express = require('express')
#Schemas= require '../DB/schema/Shemas.js'
Goal = require './DB/goal/goalNode.coffee'
User= require './DB/user/userNode.coffee'
Schedule= require './DB/sched/schedNode.coffee'
Record= require './DB/record/recordNode.coffee'
#User = require './db/UserNode.coffee'

cors = require('cors')
app = express()

app.use (req, res, next) ->
	res.header 'Access-Control-Allow-Origin', '*'
	res.header 'Access-Control-Allow-Headers',
		'Origin, X-Requested-With, Content-Type, Accept'
	res.header 'Access-Control-Allow-Methods', 'POST, GET, DELETE'
	next()
	return

app.use express.json()
# to support JSON-encoded bodies
app.use express.urlencoded()
# to support URL-encoded bodies

new Goal(app)
new User(app)
new Schedule(app)
new Record(app)

console.log config.db
mongoose.connect config.db
port = 3030
app.listen port, ->
	console.log 'Example app ;listening on port ' + port + '!'
	return
