BaseNode = require '../BaseNode.coffee'
Schemas= require '../Schem.js'
logger = require 'log4js'
log = logger.getLogger('GoalNode')
log.level='debug'

class GoalNode extends BaseNode
	path:"/goal"
	kind:'Goal'
	constructor: (app) ->
		super(app)
		@schema=Schemas.goal
		# maybe i'm duplicating features of mongooose?
		@defParent=
			#schema:Schemas.user
			# id is for dev purposes only
			id:'5adcefbaed9d970d42d33d65'
			kind:'User'
			child:'goal_ids'

	#setterParams:(req)->
	@get_by_id: (id) ->
		Schemas.goal.find _id:id
			.then (node)->
				log.info 'db returned: ',node
				return node
	
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
	
module.exports=GoalNode
