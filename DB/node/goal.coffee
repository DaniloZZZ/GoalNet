BaseNode = require './BaseNode.coffee'

class GoalNode extends BaseNode
	constructor: (args) ->
		super(args)
		@endpoint+='goal/'
		console.log @endpoint
		@type='Goal'
	
module.exports=GoalNode
