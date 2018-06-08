// This code was generated with ProjectBoot

var mongoose=require('mongoose');
var goalSchem =require("./goal/goal.js");
var commentSchem =require("./comment/comment.js");
var statSchem =require("./stat/stat.js");


module.exports={
 goal:mongoose.model('goal',goalSchem),
 comment:mongoose.model('comment',commentSchem),
 stat:mongoose.model('stat',statSchem),
}
