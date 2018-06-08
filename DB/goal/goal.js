
// this code is automatically created by ProjectBoost

var mongoose = require('mongoose');
var Schema = mongoose.Schema;
goalSchema = Schema(

{
"title":String,
"done":Boolean,
"desc":String,
}
,{collection: 'goal'}
);

module.exports = {
    goalSchema:goalSchema,
}
