import Dexie from 'dexie'

db = new Dexie('GoalNet')
db.version(1).stores
  sessions: 'user_id, logged_in'

export save_session = (user_id)->
  db.sessions.add
    user_id:    user_id
    time:       "test_time"

export get_sessions = ->
  sessions = db.sessions.toArray()
  Dexie.waitFor(sessions)
  return sessions

