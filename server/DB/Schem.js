// This code was generated with ProjectBoot

 var mongoose=require('mongoose');
 var baseSchem = require('./baseSchem.js').baseSchem
 var authkeySchem = require("./authkey/authkey.js"); 
 var goalSchem = require("./goal/goal.js"); 
 var recordSchem = require("./record/record.js"); 
 var userSchem = require("./user/user.js"); 
 var commentSchem = require("./comment/comment.js"); 
 var scheduleSchem = require("./sched/schedule.js"); 
 var statSchem = require("./stat/stat.js"); 


module.exports={ 
 authkey:mongoose.model('authkey', mongoose.Schema(Object.assign(authkeySchem,baseSchem))), 
 goal:mongoose.model('goal', mongoose.Schema(Object.assign(goalSchem,baseSchem))), 
 record:mongoose.model('record', mongoose.Schema(Object.assign(recordSchem,baseSchem))), 
 user:mongoose.model('user', mongoose.Schema(Object.assign(userSchem,baseSchem))), 
 comment:mongoose.model('comment', mongoose.Schema(Object.assign(commentSchem,baseSchem))), 
 schedule:mongoose.model('schedule', mongoose.Schema(Object.assign(scheduleSchem,baseSchem))), 
 stat:mongoose.model('stat', mongoose.Schema(Object.assign(statSchem,baseSchem))),
}
