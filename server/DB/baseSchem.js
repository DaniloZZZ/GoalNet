
var mongoose = require('mongoose')
var Schema = mongoose.Schema

// TODO: make baseSchem also generated from yaml?
var baseSchem = {
	parent:{
		kind:String,
		item:{
			type:Schema.Types.ObjectId,
			refPath:'parent.kind'
		},
	}
}
module.exports={
	baseSchem:baseSchem
}
