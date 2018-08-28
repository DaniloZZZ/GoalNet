import axios from 'axios'

BaseNode = require './BaseNode.coffee'
import SchedNode from './sched.coffee'

class GoalNode extends BaseNode
	kind:'Goal'
	endpoint:BaseNode.apibase + 'goal/'
	constructor: (args) ->
		super(args)

	onSuccess: BaseNode.onSuccess('goal')

	get_sched: (goal_id)->
		params=
			id:goal_id
		axios.get @endpoint+'sched/', params:params
			.catch @onError
			.then @onSuccess
			.then SchedNode.convertToStartEnd

	create_with_schedule:(user_id,props,schedules)->
		console.log "Creating goal and saving schedule for it"
		console.log props, schedules
		@set user_id, props
		.then( (goal)->
			if schedules
				schedNode = new SchedNode
				schedulesParent = schedules.map (s)->
					s.parent=
						kind:'Goal'
						item:goal._id
					s
				console.log(schedulesParent)
				schedNode.save_arr(schedulesParent)
		).catch (err)=> console.error err
export default GoalNode
