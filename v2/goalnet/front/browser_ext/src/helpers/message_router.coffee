
export default Router = (message_sink)->({key,routes,fallback})->
  return (...args)->
    {message, respond} = message_sink(...args)
    path = message[key]
    handler = fallback
    for route, handler_ of routes
      if route==path
        handler = handler_
    p = new Promise (resolve, reject)->
      resolve handler message
    p.then respond
    return true




