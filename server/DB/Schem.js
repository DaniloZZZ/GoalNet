// This code was generated with ProjectBoot

 var mongoose=require('mongoose');
 var baseSchem = require('./baseSchem.js').baseSchem
 var goalSchem = require("./goal/goal.js"); 
 var userSchem = require("./user/user.js"); 
 var commentSchem = require("./comment/comment.js"); 
 var scheduleSchem = require("./sched/schedule.js"); 
 var statSchem = require("./stat/stat.js"); 


module.exports={ 
 goal:mongoose.model('goal', mongoose.Schema(Object.assign(goalSchem,baseSchem))), 
 user:mongoose.model('user', mongoose.Schema(Object.assign(userSchem,baseSchem))), 
 comment:mongoose.model('comment', mongoose.Schema(Object.assign(commentSchem,baseSchem))), 
 schedule:mongoose.model('schedule', mongoose.Schema(Object.assign(scheduleSchem,baseSchem))), 
 stat:mongoose.model('stat', mongoose.Schema(Object.assign(statSchem,baseSchem))),
}
