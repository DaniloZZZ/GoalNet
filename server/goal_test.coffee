chai = require 'chai'
mocha = require 'mocha'
chai.should()

GoalNode =require '../node/goal.coffee'
describe 'goalNode', ->
	goal = new GoalNode()
	it 'should have an appropriate endpoint',->
		goal.endpoint.should.equal \
		'http://lykov.tech/goalnet/goal/'
	it 'should get goal', (done)->
		goal.get('5ade5fffeca9285e7fc01003','')
			.then (resp)->
				console.log resp
				done()
			.catch console.log
		return

