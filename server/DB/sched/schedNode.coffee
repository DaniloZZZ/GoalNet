BaseNode = require '../BaseNode.coffee'
Schemas= require '../Schem.js'

class SchedNode extends BaseNode
	path:"/schedule"
	kind:'Schedule'
	constructor: (app) ->
		super(app)
		@schema=Schemas.schedule
		# maybe i'm duplicating features of mongooose?
	
	@add_comment:(req)->
		q = req.query
		goal_id=q.id
		text=q.text
		# Now add a comment to db
		"""
		new Promise (resolve,reject)=>
			Schemas.Comment.find(
				'parent.item':id
			)
			.then (goals)->
				log.debug goals
				resolve goals
		"""
	
module.exports=SchedNode
