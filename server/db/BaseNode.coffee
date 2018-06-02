logger = require 'log4js'
log = logger.getLogger('DB-baseNode')
log.level='debug'


class BaseNode
	#apibase='http://lykov.tech/goalnet/'
	constructor: (app) ->
		# TODO: raise an error if no params provided
		@app=app
	schema:null
	path:null

	type:'NOTYPE'

	@onConnect: (req)->
		# this depends on server api
		log.info req.url, 'got connection ',req.headers.host
		log.debug req.headers

	@onError: (err)->
		log.error 'error db',err
		# this depends on db api
		return err.name

	registerAppEndpoints:()->
		@app.route @path
			.get @regCallback @get
			.post @regCallback @set

	# This method is connection with db.
	# If changed db you should edit _it_
	get: (req)=>
		#TODO: add projection support
		id=req.query.id
		new Promise (resolve,reject)=>
			@schema.find
				_id:id
				(err,node)->
					if err
						reject err
					else
						log.info 'db returned: ',node
						resolve node

	set: (req)=>
		#TODO: add projection support
		# TODO: add update metho
		id:req.query.id
		props:req.body
		new Promise (resolve,reject)=>
			node = new @schema props
			node.save (err)->
				if err
					reject err
				else
					log.info 'db returned: ',err
					resolve 'OK'

	# wraps with logging methods
	regCallback: (dbcall)-> (req,res)->
			BaseNode.onConnect(req)
			#TODO: add conversion from api to db	
			dbcall(req)
			.then (r)=>res.send r
			.catch (err)=>
				res.status 400
				res.send BaseNode.onError err

module.exports=BaseNode
