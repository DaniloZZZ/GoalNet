baseTests = require('../../test/baseNode.coffee')
SchedNode =require '../schedNode.coffee'
GoalNode =require '../../goal/goalNode.coffee'
chai = require 'chai'
chai.should()

express = require 'express'
mongoose = require('mongoose')
log4js = require 'log4js'
logger = log4js.getLogger('test')
logger.level = 'debug'

# configure a testing server
app = express()
app.use express.json()
app.use express.urlencoded()
mongoCred=process.env.MONGO_CREDENTIALS
mongoose.connect "mongodb://"+mongoCred+
	"@lykov.tech:27017/goalnet"

sched = new SchedNode(app)
goal = new GoalNode(app)
port = 3030
host = 'localhost'
endpoint = "http://#{host}:#{port}"
server=null
start=()->
	server = app.listen port, ->
		logger.info 'Test app is listening '+ endpoint
		return

# Start testing
describe 'Schedule', ->
	before start
	after ()->server.close()
	sched_= {}
	describe 'basics', ->
		it 'should have an appropriate endpoint',->
			sched.path.should.equal '/schedule'

		it 'should save schedule',(done)->
			baseTests.set(sched,props: type:'test')()
			.then (u)=>
				sched_=u
				done()
			return
		it 'should get schedule',()->
			baseTests.get(sched,id:sched_._id)()
		it 'should delete schedule',()->
			baseTests.delete(sched,id:sched_._id)()
