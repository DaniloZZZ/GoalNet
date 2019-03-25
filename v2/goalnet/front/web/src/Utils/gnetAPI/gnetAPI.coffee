import Promise from 'promise'
import moment from 'moment'
import {Connector} from '../websockets/connector.coffee'

export default class GnetAPI extends Connector
  constructor: (props)->
    super(props)
    console.log 'GNEAPI', props
    {@uid} = props
    @triggers = {}
    @add_callback @callback
    
  set_uid:(uid)->
    console.log "GnetAPI uid",uid
    @uid = uid

  callback:(message)=>
    console.log 'api got', message
    {action} = message
    for act, trig of @triggers
      if act == "*" or act==action
        trig message
  add_trigger:(name,trig)->
    @triggers[name]=trig

  add_record:(name)->
    @send
      action:'add.webext.record'
      name:name
  get_integral_metrics:({name, end, start})->
    console.log 'getting integral metrics of', name
    @send
      action:'get.webext.metrics'
      name:'integral'
      providers:[name]
      end:end
      start:start
      step:200

  get_connectors:(clb)->
      console.log 'getting connectors of',@uid
      @send action:'get.user.module'
      @add_trigger 'user.modules', clb
  add_connector:(name)->
      console.log 'adding connector of',@uid
      @send action:'add.user.module',name:name
     

