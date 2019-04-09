host = 'lykov.tech'
host = 'localhost'
apipath = "ws://"+host+":3032"

STATES=
  Open:'open'
  Closed:'closed'
  Error:'error'
  Init:'init'

export default class GoalNetApi
  constructor:(props)->
    ws = new WebSocket(apipath)
    @state = STATES.Init
    ws.onopen = => @state = STATES.Open
    ws.onclose = => @state = STATES.Closed
    ws.onerror = => @state = STATES.Error
    @ws = ws
    auth =
      token:props.token
      action:'get.user.module'
    console.log 'auth with token', auth
    sendm = =>
      msg = JSON.stringify auth
      console.log 'sending message', msg
      console.log 'websocket', @ws
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

