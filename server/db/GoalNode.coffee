BaseNode = require './BaseNode.coffee'
Schemas= require './Shemas.js'

class GoalNode extends BaseNode
	constructor: (app) ->
		super(app)
		@path='/goal'
		@schema=Schemas.Goal
		# maybe i'm duplicating features of mongooose?
		@type='Goal'
	
module.exports=GoalNode
