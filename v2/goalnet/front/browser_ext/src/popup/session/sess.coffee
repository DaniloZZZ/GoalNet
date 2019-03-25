import Promise from 'promise'
if chrome
  browser=chrome
  
export save_session = (token)->
  new Promise (resolve, reject)->
    browser.runtime.sendMessage
      action:'set.session'
      token:token
      resolve

export get_session = ()->
  new Promise (resolve, reject)->
    browser.runtime.sendMessage
      action:'get.session'
      resolve



