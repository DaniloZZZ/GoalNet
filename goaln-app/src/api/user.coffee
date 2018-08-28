BaseNode = require './BaseNode.coffee'
SchedNode = require './sched.coffee'
import axios from 'axios'
class UserNode extends BaseNode
	kind:'User'
	endpoint:BaseNode.apibase + 'user/'
	constructor: (args) ->
		super(args)
	
	get_sched: (user_id)->
		params=
			id:user_id
		axios.get @endpoint+'sched/', params:params
			.then @onSuccess
			.then SchedNode.convertToStartEnd

	get_goals: (user_id)->
		params=
			id:user_id
		axios.get @endpoint+'goals/', params:params
			.catch @onError
			.then @onSuccess

export default UserNode
