GoalNode =require '../goalNode.coffee'
chai = require 'chai'
chai.should()
axios = require 'axios'
express = require 'express'
log4js = require 'log4js'
mongoose = require('mongoose')
logger = log4js.getLogger('test')
logger.level = 'debug'

logger.info "hello tester!"
app = express()
app.use express.json()
app.use express.urlencoded()
mongoCred=process.env.MONGO_CREDENTIALS
mongoose.connect "mongodb://"+mongoCred+
	"@lykov.tech:27017/goalnet"
goal = new GoalNode(app)
port = 3030
server=null
start=()->
	server = app.listen port, ->
		logger.info 'Test app is listening '+port
		return

describe 'goalNode', ->
	before start
	after ()->server.close()
	goal_= {}
	endpoint = "http://lykov.tech:"+port
	it 'should have an appropriate endpoint',->
		goal.path.should.equal '/goal'

	it 'should save goal', () ->
		axios.post(
			endpoint+'/goal/',
			props:
				title:"a test goal"
				desc:"some arbitrary descdlkfjasl"
				done: false
		)
		.then( (resp)->
			logger.debug resp.data
			goal_=resp.data
		).catch (err)=> logger.error err

	it 'should get goal', (done)->
		axios.get(
			endpoint+'/goal/'
			params:
				id:goal_._id
		)
		.then (resp)->
			logger.debug resp.data
			done()
		.catch (err)=> logger.error err
		return

	it 'should delete goal', (done)->
		axios.delete(
			endpoint+'/goal/'
			params:
				id:goal_._id
		)
		.then (resp)->
			logger.debug resp.data
			done()
		.catch (err)=> logger.error err
		return


