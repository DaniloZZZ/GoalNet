React = require 'react'
ReactDOM = require 'react-dom'
moment = require 'moment'

import DOM from 'react-dom-factories'
config =  require process.env.GOALNET_CONFIG_FILE
import { Form, Text, TextArea, Checkbox } from 'react-form'
import Canvas from './canvas.coffee'

axios =  require 'axios'

{Component}= React
L_ = React.createElement
L = DOM
l = console.log

Router = require('react-router')
Route = Router.Route

class Picker extends Component
	constructor: (props)->
		super()
		@state =
			dates:[]
			children:[]

	get_user_data: (id) ->
		_=this

	sendReq: =>
		val = document.getElementById('inp').value
		axios.get config.server+'/setlong/',
			params:
					val:val
		.then (g) =>
			console.log('long',g)
			@setState(elecval:g.data)

	new_comment: ->
		uid =  @state.uid
		gid =  @state.gid

	itemCreate: (item) =>
		l 'new item',item
		Object.assign(item,id:@state.children.length+1)
		@setState
			children:@state.children.concat(item)


	render: ->
		L.div
			className:'picker'
			style:
				backgroundColor:'blue'
				posirion:'relative'
				height:'200px'
				width:'200px'
			L_ Canvas,
				kak:'afaasdfa'
				idx:12
				children:@state.children
				onItemCreate:@itemCreate
			L.div
				style:
					height:'100px'
					width:'100px'
					backgroundColor:'green'
				onMouseDown:@sendReq
				@state.elecval
				L.input type:'text',id:'inp'


export default Picker
	
