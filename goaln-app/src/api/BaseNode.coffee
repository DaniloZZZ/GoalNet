axios = require 'axios'
#logger = require 'log4js'
#log = logger.getLogger('api-baseNode')
#log.level='debug'

class BaseNode
	#apibase='http://lykov.tech/goalnet/'
	@apibase:'http://localhost:3030/'
	endpoint:BaseNode.apibase
	schema:null
	kind:'NOTYPE'

	constructor: (args) ->
		console.log "endpoint for #{@kind} is ", @endpoint
		@onSuccess = BaseNode.onSuccess(@kind)
		@onError = BaseNode.onError(@kind)
		if not args
			return
		if args.verbose
			console.log "Hey, new BaseNode created"

	@onError: (kind)-> (err)->
		console.error "while requesting #{kind}", err
		if err.response
			console.error err.response.status,
			"request for #{kind} failed"
			console.log err.response.headers
			console.log err.response.data
	@onSuccess: (kind)->(resp)->
		if resp
			console.log "request for #{kind} successfull"
			resp.data
		else
			console.log "request for #{kind} returned null"
			[]


	# Method to get an abstract node of data
	# and project it to some subset of props
	get: (id,proj)->
		new Promise (resolve,reject)=>
			console.log 'getting,',id,proj
			console.log 'request for',@kind,' id ',id
			if proj
				params=id:id,project:proj
			else
				params=id:id
			axios.get @endpoint, params:params
			.then (resp) => resolve @onSuccess resp
			.catch @onError

	set: (id,props)=>
		# Method for saving or modifying the node
		# Server will search and update if id exissts.
		# For mor fast updating use update(unimpl)
		new Promise (resolve,reject)=>
			console.log 'setting(saving),',id
			console.log 'request for',@kind,' id ',id
			axios.post @endpoint,
				id:id
				props:props
			.then (resp) => resolve @onSuccess resp
			.catch @onError
	# TODO: add update metho

module.exports=BaseNode
