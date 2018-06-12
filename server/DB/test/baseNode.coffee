axios = require 'axios'
log4js = require 'log4js'
logger = log4js.getLogger('test')
logger.level = 'debug'

port = 3030
host = 'localhost'
endpoint = "http://#{host}:#{port}"
module.exports={
	get:(node,props)->()->
		axios.get(
			endpoint+node.path
			params:props
		)
		.then (resp)->
			logger.debug resp.data
			resp.data
		.catch (err)=> logger.error err

	set:(node,data)->()->
		axios.post(
			endpoint+node.path
			data
		)
		.then (resp)->
			logger.debug resp.data
			resp.data
		.catch (err)=> logger.error err

	delete:(node,params)->()->
		axios.delete(
			endpoint+node.path
			params:params
		)
		.then (resp)->
			logger.debug resp.data
		.catch (err)=> logger.error err

}
