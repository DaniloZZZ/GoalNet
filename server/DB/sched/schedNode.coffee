log4js = require 'log4js'
logger = log4js.getLogger('Sched Node')
logger.level = 'debug'
BaseNode = require '../BaseNode.coffee'
Schemas= require '../Schem.js'
notif = require '../NotifApi.coffee'

class SchedNode extends BaseNode
	path:"/schedule"
	kind:'Schedule'
	constructor: (app) ->
		super(app)
		@schema=Schemas.schedule
		@router.post '/set_array', @genCallbackFun @set_array
		# maybe i'm duplicating features of mongooose?
	setterParams:(req)->
		ret =
			parent:@defParent||req.body.props.parent
			props:req.body.props
			_id:req.body.id
		ret
	
	set_array: (req)=>
		#TODO: add update method
		if not Array.isArray( req.body)
			logger.error('client provided not an array')
			return 'Please provide an array'
		return new Promise( (resolve,reject)=>
			count = req.body.length
			nodes=[]
			req.body.forEach((el)=>
				params = el
				#params._id = el.id
				node = new @schema params
				logger.info("saving #{@kind}...")
				logger.debug('item:',node)
				node.save()
					.then (node)=>
						logger.info 'Node saved. '
						logger.debug node
						notif.scheduleUpdate(node)
							.then (resp)->
								nodes.push(node)
								if nodes.length==count
									resolve nodes
								)

		)

	#TODO:want to update parant's children field?
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
