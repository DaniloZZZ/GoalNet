axios = require 'axios'
logger = require 'log4js'
log = logger.getLogger('api-baseNode')
log.level='debug'

class BaseNode
	#apibase='http://lykov.tech/goalnet/'
	apibase='http://localhost:3030/'
	constructor: (args) ->
		if not args
			return
		if args.verbose
			log.info "Hey, new BaseNode created"

	endpoint:apibase
	schema:null
	type:'NOTYPE'

	onError: (err)->
		log.error err.response.status, ',request failed'
		log.debug err.response.headers
		log.debug err.response.data
	
	netwok: (method)->

	# Method to get an abstract node of data
	# and project it to sum subset of props
	get: (id,proj)->
		new Promise (resolve,reject)=>
			log.debug 'getting,',id,proj
			log.debug 'request for',@type,' id ',id
			if proj
				params=id:id,project:proj
			else
				params=id:id
			axios.get @endpoint, params:params
			.then (resp) -> resolve resp.data
			.catch @onError

	set: (id,props)=>
		# Method for saving or modifying the node
		# Server will search and update if id exissts.
		# For mor fast updating use update
		new Promise (resolve,reject)->
			log.debug 'setting(saving),',id,proj
			log.debug 'request for',@type,' id ',id
			axios.post @endpoint,
				id:id
				props:props
			.then (resp) -> resolve resp.data
			.catch @onError
	# TODO: add update method

module.exports=BaseNode
