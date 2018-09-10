log4js = require 'log4js'
logger = log4js.getLogger('Record Node')
logger.level = 'debug'
BaseNode = require '../BaseNode.coffee'
Schemas= require '../Schem.js'
notif = require '../NotifApi.coffee'

class RecordNode extends BaseNode
	path:"/record"
	kind:'Record'
	constructor: (app) ->
		super(app)
		@schema=Schemas.record
		# maybe i'm duplicating features of mongooose?
	setterParams:(req)->
		logger.info(req.body)
		ret =
			parent:@defParent||req.body.parent
			props:req.body.props
			_id:req.body.id
		ret

	#TODO:want to update parant's children field?
	@add_comment:(req)->
		q = req.query
		goal_id=q.id
		text=q.text
		# Now add a comment to db
		"""
		"""
	
module.exports=RecordNode
