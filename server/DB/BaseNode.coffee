logger = require 'log4js'
express = require 'express'
log = logger.getLogger('DB-baseNode')
log.level='debug'


class BaseNode
	#apibase='http://lykov.tech/goalnet/'
	schema:null
	path:""
	kind:'NOTYPE'

	constructor: (app) ->
		# TODO: raise an error if no params provided
		@app=app
		@router = express.Router()
		@router.get '/', @genCallbackFun @get
		@router.post '/', @genCallbackFun @set
		@router.delete '/', @genCallbackFun @delete
		log.info 'Starting router for ', @kind
		@app.use(@path,@router)

	@onConnect: (req)->
		# this depends on server api
		log.info req.url, 'got connection ',req.headers.host
		log.debug req.headers

	@onError: (err)->
		log.error 'error db',err
		# this depends on db api
		return err.name

	getterParams:(req)->
		_id:req.query.id
	setterParams:(req)->
		ret =
			parent:@defParent||req.body.props.parent
			props:req.body.props
			_id:req.body.id
		ret
	deleterParams:(req)->
		_id:req.query.id


	# This method is connection with db.
	# If changed db you should edit _it_
	get: (req)=>
		#TODO: add projection support
		params = @getterParams(req)
		log.debug('finding...')
		@schema.find params
			.then (node)->
				log.info "db returned for params#{JSON.stringify(params)}: ",node
				return node

	set: (req)=>
		#TODO: add update method
		params = @setterParams req
		newProps=params.props ||{}
		node = new @schema newProps
		if params.parent
			node.parent.kind =params.parent.kind
			node.parent.item =params.parent.id
		log.info("saving #{@kind}...")
		node.save()
			.then (node)=>
				log.info 'Node saved. '
				log.debug node
				return node
	#TODO:want to update parant's children field?

	delete: (req)=>
		params = @deleterParams(req)
		log.debug('deleting...')
		@schema.deleteOne(params)
			.then (node)->
				log.info 'Node deleted. '
				log.debug node
				return node

	# wraps  dbcall with with logging
	genCallbackFun : (dbcall)-> (req,res)->
			BaseNode.onConnect(req)
			#TODO: add conversion from api to db (need?)
			dbcall(req)
			.then (r)=>
				res.send r
				log.info 'sent response',r
			.catch (err)=>
				res.status 400
				res.send BaseNode.onError err

module.exports=BaseNode
