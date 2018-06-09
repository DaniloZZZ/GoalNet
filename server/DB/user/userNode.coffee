logger = require 'log4js'
log = logger.getLogger('DB-userNode')
log.level='debug'

BaseNode = require '../BaseNode.coffee'
Schemas = require '../Schem.js'
GoalNode= require '../goal/goalNode.coffee'

class UserNode extends BaseNode
	path:'/user'
	schema:Schemas.user
	kind:'User'
	constructor: (app) ->
		super(app)
		# maybe i'm duplicating features of mongooose?
		@defParent=
			null
		@router.get '/sched', @genCallbackFun @get_sched
		@router.get '/goals', @genCallbackFun @get_goals

	#setterParams:(req)->
	
	get_goals:(req)->
		id=req.query.id
		Schemas.goal.find(
			'parent.item':id
		)
		.then (goals)->
			log.debug goals
			return goals
	
	#TODO: Use GraphQL for populating
	get_sched:(req)=>
		id=req.query.id
		log.info id
		new Promise (resolve,reject)=>
			@get_goals req
			.then (goals)->
				res = []
				# for each goal of user 
				for goal in goals
					log.debug goal
					# find schedule of the goal
					Schemas.sched.find(
						'parent.item':goal._id
					)
					.then (s)->
						# and concat it into result
						res= res.concat(s)
						if res.length==goals.length
							# TODO: pass it through condition checker
							log.info 'got sched for user',res
							resolve res

module.exports=UserNode
