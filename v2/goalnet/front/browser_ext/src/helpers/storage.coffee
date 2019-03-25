import GoalNetApi from './goalnet.coffee'

export class Storage
  constructor:(props)->
    console.log 'storage init'
    self.db = []

  put_item:(item)->
    self.db.push(item)
  get_item:(idx)->
    self.db[idx]
  get_all:(idx)->
    self.db


export default class CachedStorage extends Storage
  constructor:(props)->
    super(props)
    @cache = []
    @cache_len = 10
  set_api:(api)->
    @api = api

  put_item:(item)->
    console.log 'put item', item
    super.put_item()
    if @cache.length==@cache_len
      @cache.shift()
    @cache.push(item)
    @api?.send_web_record(item)

  get_last_item:()->
    @cache.slice(-1)[0]




