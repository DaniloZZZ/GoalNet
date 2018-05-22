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
			log.debug @endpoint, apibase,@type,params
			axios.get @endpoint, params:params
			.then (resp) ->
				if resp.status==200
					log.info 'request successfull. id ',id
					resolve resp.data
				else
					log.error 'error getting ',@type, id
					reject resp
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
			.then (resp) ->
				if resp.status==200
					log.info 'request successfull. id ',id
					resolve resp.data
				else
					log.error 'error getting ',@type, id
					reject resp
			.catch @onError

module.exports=BaseNode
