baseTests = require('../../test/baseNode.coffee')
UserNode =require '../userNode.coffee'
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
user = new UserNode(app)
port = 3030
host = 'localhost'
endpoint = "http://#{host}:#{port}"
server=null
start=()->
	server = app.listen port, ->
		logger.info 'Test app is listening '+ endpoint
		return

describe 'userNode', ->
	before start
	after ()->server.close()
	user_= {}
	it 'should have an appropriate endpoint',->
		user.path.should.equal '/user'

	it 'should save user',(done)->
		baseTests.set(user, name:'user',lname:'test')()
		.then (u)=>
			user_=u
			done()
		return

	it 'should get user',()->
		baseTests.get(user,id:user_._id)()

	it 'should delete user',()->
		baseTests.delete( user,id:user_._id)()

