
// this code is automatically created by ProjectBoost

var mongoose = require('mongoose');
var Schema = mongoose.Schema;
commentSchema = Schema(

{
"author":Schema.Types.ObjectId,
"text":String,
"date":Date,
}
,{collection: 'comment'}
);

module.exports = {
    commentSchema:commentSchema,
}
