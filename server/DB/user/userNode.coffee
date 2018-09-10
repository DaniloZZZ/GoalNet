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
		@router.get '/records', @genCallbackFun @get_records

	#setterParams:(req)->
	get_records:(req)->
		id=req.query.id
		filter = req.query.filter
		log.warn 'filter', filter
		log.info 'finding records of ',id
		dic = {
				...{'parent.item':id},
				...JSON.parse(filter)
			}
		log.warn dic
		Schemas.record.find(
			dic
		).sort( date:-1 ).limit(3)
		.then (records)->
			log.debug records
			return records
	get_goals:(req)->
		id=req.query.id
		log.info 'finding goals of ',id
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
					# find schedule of the goal
					s = await Schemas.schedule.find(
						'parent.item':goal._id
					)
					# and concat it into result
					log.info('atom got',s)
					res= res.concat(s)
							# TODO: pass it through condition checker
					log.info "got scheds for goal#{goal._id}",res
				resolve res

module.exports=UserNode
