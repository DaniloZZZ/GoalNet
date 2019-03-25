apipath = "ws://127.0.0.1:3032"

export default class GoalNetApi
  constructor:(props)->
    @ws = new WebSocket(apipath)
    auth =
      token:props.token or 'machine'
    console.log 'auth with token', auth
    sendm = =>
      msg = JSON.stringify auth
      console.log 'msg', msg
      console.log 'ws', @ws
      @ws.send msg
    setTimeout sendm, 100

  send_web_record:(record)->
    web_rec = 'test.record'
    action =
      action:'put.'+web_rec
      name:'websites'
      value:record.domain
      time:record.time
    console.log 'sending to gnet', action
    message = JSON.stringify(action)
    @ws.send message

