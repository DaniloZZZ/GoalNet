import axios from 'axios'
moment = require 'moment'
BaseNode = require './BaseNode.coffee'

class SchedNode extends BaseNode
	kind:'Schedule'
	endpoint:BaseNode.apibase + 'schedule/'
	constructor: (args) ->
		super(args)

	save_arr:(arr)->
		axios.post @endpoint+'set_array', arr

	@convertToStartEnd:(data)->
		console.log 'before',data
		conv=(sch)->
			i = sch.timeline
			r = {}
			r.start = i.start
			r.end = i.start+moment().seconds(i.duration)
		res = data.map(conv)
		console.log 'conv',res
		res
	
export default SchedNode
