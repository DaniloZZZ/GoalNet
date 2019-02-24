import {get_sessions, save_session} from '../DB/db.coffee'

export logged_in = ()->
  console.log("checking if user is logged in")
  sessions = await get_sessions()
  session = sessions[0]
  console.log 'ss',session
  if session
    return session.user_id
  else
    return false

export debug_login = ()->
  save_session('1')
