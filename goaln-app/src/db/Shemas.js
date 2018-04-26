var mongoose = require('mongoose')
console.log(mongoose.Shema)

var userShem = mongoose.Schema({
	fname: String,
	lname: String,
	login: String,
	pass: String,
	avatar: String,
	goal_ids: [ String ],
},{collection:'Users'})

var goalShem = mongoose.Schema({
	title: String,
	deadline: Date,
	desc: String,
	done: Boolean,
},{collection:'Goals'})

module.exports = {
	Goal:mongoose.model('Goal',goalShem),
	User:mongoose.model('User',userShem)
}
