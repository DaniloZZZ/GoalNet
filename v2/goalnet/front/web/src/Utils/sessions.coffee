import {remove_session, get_sessions, save_session} from '../DB/db.coffee'
import jwt from 'jsonwebtoken'

export logged_in = ()->
  console.log("Getting sessions from db...")
  sessions = await get_sessions()
  session = sessions[0]
  console.log 'Current session:',session
  if session
    return session.user_id
  else
    # check if there is a cookie token
    token = getCookie('token')
    console.log 'token', token
    if token
      data = jwt.decode(token)
      return data.user_id

    return false

export log_out = ()->
  deleteAllCookies()
  await remove_session()

export debug_login = ()->
  save_session('1')
getCookie=(name) ->
  matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ))
  return if matches then decodeURIComponent(matches[1]) else undefined

deleteAllCookies = ->
  console.log 'delc'
  document.cookie = 'token="", expires=Thu, 01 Jan 1970 00:00:01 GMT;'
