import {extractDomain} from '../helpers/webtime.coffee'
import CachedStorage from '../helpers/storage.coffee'
import GoalNetApi from '../helpers/goalnet.coffee'
import Router from '../helpers/message_router.coffee'

if chrome
  browser=chrome

console.log "background"

storage = new CachedStorage()
browser.storage.local.get 'session',(result)=>
  console.log 'got session', result
  api = new GoalNetApi token:result.session?.token
  storage.set_api api
TIMEOUT_S = 20*1000
timeoutId = 0


userIdle=()->
  event =
    domain:'away'
    time:Date.now()/1000
  storage.put_item(event)

handlePageEvent=(event)->
  url = event.url
  domain = extractDomain(url)
  if timeoutId
    clearTimeout(timeoutId)
  timeoutId = setTimeout userIdle, TIMEOUT_S

  last_item = storage.get_last_item()
  if last_item
    if last_item.domain==domain
      return
  event =
    domain:domain
    time:Date.now()/1000
  storage.put_item(event)

webextRouter = Router (request, sender, sendResponse)->
  if sender.tab
    console.log 'message from a content script:', sender.url
  else
    console.log 'message from the ext:',request
  request['url'] = sender.url
  return message:request,respond:sendResponse

listener = webextRouter
    key:'action'
    routes:
      'post.event':(msg)->
        event =
          url:msg.url
          type:msg.event_type
        handlePageEvent event
      'get.event':(msg)-> storage.get()
      'set.session':(msg)->
        if msg.token?
          browser.storage.local.set session: token:msg.token
        else
          console.error 'wrong set session req'
      'get.session':(msg)->
        new Promise (resolve,reject)->
          browser.storage.local.get 'session',(result)=>
            console.log 'got session', result
            resolve result
    fallback:
        (msg)->error:'Wrong action'

browser.runtime.onMessage.addListener listener

