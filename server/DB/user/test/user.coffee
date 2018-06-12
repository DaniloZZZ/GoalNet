baseTests = require('../../test/baseNode.coffee')
UserNode =require '../userNode.coffee'
GoalNode =require '../../goal/goalNode.coffee'
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
goal = new GoalNode(app)
port = 3030
host = 'localhost'
endpoint = "http://#{host}:#{port}"
server=null
start=()->
	server = app.listen port, ->
		logger.info 'Test app is listening '+ endpoint
		return

describe 'userNode, basic', ->
	before start
	after ()->server.close()
	user_= {}
	it 'should have an appropriate endpoint',->
		user.path.should.equal '/user'

	it 'should save user',(done)->
		baseTests.set(user,props: name:'user',lname:'test')()
		.then (u)=>
			user_=u
			done()
		return

	it 'should get user',()->
		baseTests.get(user,id:user_._id)()

	it 'should delete user',()->
		baseTests.delete( user,id:user_._id)()

describe.only 'userNode, specific', ->
	before start
	#after ()->server.close()
	user_= {_id:'5adcefbaed9d970d42d33d65'}

	describe 'should get user goals',()->
		num = 2
		it 'saves some goals for user', (done)->
			cnt = 0
			g=(num_)->
				for i in [1..num_]
					f = baseTests.set goal,
						props:
							title:'testgoal'+i
							parent: item:user_._id,kind:'user'
					f().then ()->
						cnt+=1
						if cnt==num
							logger.warn 'hfalhl'
							done()
			g num
			return
		it 'gets the same number of goals', (done)->
			axios.get(
				endpoint+'/user/goals/'
				params:
					id:user_._id
			)
			.then (resp)->
				logger.debug resp.data
				resp.data.length.should.equal num
				done()
			.catch (err)=> logger.error err
			return

