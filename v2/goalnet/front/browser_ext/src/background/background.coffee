import {extractDomain} from '../helpers/webtime.coffee'
import CachedStorage from '../helpers/storage.coffee'

if chrome
  browser=chrome

console.log "background"

storage = new CachedStorage()
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



browser.runtime.onMessage.addListener (request, sender, sendResponse) ->
    if sender.tab
      console.log 'fron a content script:', sender.url
    else
      console.log 'from the ext'
    [action, trait] = request.action.slpit('.')
    if trait = 'event'
      if action=='post'
        event =
          url:sender.url
          type:request.event_type
        handlePageEvent event
        
      if action=='get'
        data = storage.get()
        sendResponse data

