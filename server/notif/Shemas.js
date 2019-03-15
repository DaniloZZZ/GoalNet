var mongoose = require('mongoose')
var Schema = mongoose.Schema

var baseShem = {
	parent:{
		kind:String,
		item:{
			type:Schema.Types.ObjectId,
			refPath:'parent.kind'
		},
	}
}

var userShem = mongoose.Schema(
{
	fname: String,
	lname: String,
	login: String,
	pass: String,
	avatar: String,
	// TODO: Use virtal to populate
	goal_ids: [ String ],
}
	,{collection:'Users'})

var goalShem = mongoose.Schema(
	Object.assign(baseShem,
		{
	title: String,
	deadline: Date,
	desc: String,
	done: Boolean,
	sched:[{start:Date,end:Date,id:String}],
	comments:[{
		user_id:mongoose.Schema.Types.ObjectId, 
		text:String,
		date:Date}
]

		}
	)
		,{collection:'Goals'})

schedShem = mongoose.Schema(
  Object.assign( baseShem,
	  {
  title: String,
  done: Boolean,
  timeline:[ {
	action: Schema.Types.ObjectId,
    start: Date,
    dur: Date,
	condition_text:{
		type: String,
		default: 'every week'
	},
	condition:{
	  type:{
		  type:	    String,
		  default:	'every'
	  },
	  path:{
		  type:		String,
		  default:	'day'
	  },
	  value:{
		  type: String,
		  default: Date
	  }
	}
  }
  ]
	  })
	,
	{collection: 'Sched'})
  

module.exports = {
	Goal:mongoose.model('Goal',goalShem),
	User:mongoose.model('User',userShem),
	Sched: mongoose.model('Sched', schedShem)
}
