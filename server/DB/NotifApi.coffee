User = require('./user/userNode.coffee')
Goal = require('./goal/goalNode.coffee')
axios = require 'axios'
log4js = require 'log4js'
logger = log4js.getLogger('Notif api')
logger.level = 'debug'

API = "http://localhost:3200"

scheduleUpdate = (sch)->
	logger.info 'getting goal for schedule'
	Goal.get_by_id(sch.parent.item)
		.then (goals)->
			rec =
				type: 'schedule'
				name: 'scheduleUpdate'
				content:
					start: sch.start
					end: sch.end
				id: sch._id
			params = goal:goals[0],record:rec
			logger.info params
			# Here you should get user's H settings
			axios.post(API, params)
				.then (resp)->
					logger.info resp.url,resp.data
					resp

module.exports = scheduleUpdate:scheduleUpdate
