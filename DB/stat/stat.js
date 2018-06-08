
// this code is automatically created by ProjectBoost

var mongoose = require('mongoose');
var Schema = mongoose.Schema;
statSchema = Schema(

{
"end":Date,
"type":String,
"start":Date,
"activity":String,
}
,{collection: 'stat'}
);

module.exports = {
    statSchema:statSchema,
}
