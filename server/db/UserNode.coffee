logger = require 'log4js'
log = logger.getLogger('DB-userNode')
log.level='debug'

BaseNode = require './BaseNode.coffee'
Schemas = require '../DB/Shemas.js'

class UserNode extends BaseNode
	constructor: (app) ->
		super(app)
		@path='/user'
		@schema=Schemas.user
		# maybe i'm duplicating features of mongooose?
		@kind='User'
		@defParent=
			null
		@router.get '/sched', @regCallback @get_sched
		@router.get '/goals', @regCallback @get_goals

	#setterParams:(req)->
	
	get_goals:(req)->
		id=req.query.id
		new Promise (resolve,reject)=>
			Schemas.goal.find(
				'parent.item':id
			)
			.then (goals)->
				log.debug goals
				resolve goals
	
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
