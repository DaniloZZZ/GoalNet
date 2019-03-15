mongoose = require('mongoose')
Schema = mongoose.Schema
baseShem = parent:
  kind: String
  item:
    type: Schema.Types.ObjectId
    refPath: 'parent.kind'

userShem = mongoose.Schema({
  fname: String
  lname: String
  login: String
  pass: String
  avatar: String
  goal_ids: [ String ]
}, collection: 'Users')

goalShem = mongoose.Schema(
	Object.assign(
		baseShem,
  title: String
  deadline: Date
  desc: String
  done: Boolean
  sched: [ {
    start: Date
    end: Date
    id: String
  } ]
  comments: [ {
    user_id: mongoose.Schema.Types.ObjectId
    text: String
    date: Date
  } ]),
  collection: 'Goals')


module.exports =
  Goal: mongoose.model('Goal', goalShem)
  User: mongoose.model('User', userShem)
  Sched: mongoose.model('Sched', schedShem)

