React = require 'react'
ReactDOM = require 'react-dom'
moment = require 'moment'
import DOM from 'react-dom-factories'
config =  require process.env.GOALNET_CONFIG_FILE
import './comments.css'
import { Form, Text, TextArea, Checkbox } from 'react-form';

axios =  require 'axios'
# Assign React to Window so the Chrome React Dev Tools will work.

{Component}= React
L = DOM
l = console.log

Router = require('react-router')
Route = Router.Route

class Comments extends Component
	constructor: (props)->
		super()
		@state =
			comm:props.comments
			uid:config.def_id
			gid:props.gid
			user_data:{}
		if props.comments
			@get_user_data c.user_id for c in @state.comm

	get_user_data: (id) ->
		_=this
		l 'getting data for ', id
		axios.get config.server+'/user/',
			params:
					id:id
		.then (g) =>
			console.log('got user',g.data)
			console.log('state',@state)
			a = {}
			a[id] = g.data
			_.setState user_data: Object.assign _.state.user_data, a

	new_comment: ->
		uid =  @state.uid
		gid =  @state.gid
		(data) ->
			axios.post config.server+'/comment/',
					Object.assign
						act:'add'
						id:gid
						uid:uid
						text:data.comment
						date:moment()
			.then (g)->
				console.log('Saved comment',g.data)

	render: ->
		L.div
			className:'comments'
			L.div
				className:'comms'
					if @state.comm
						@state.comm.map (i,num)=>
							ud = @state.user_data[i.user_id]
							name = if ud
								ud.fname
							else '..'
							L.div
								className:'comm'
								key:num
								L.div style: position:'relative'
									L.div
										className:'comm-name'
										name
									L.div
										style:
											right:'0px'
											display:'inline-block'
											float:'right'
											position:'relative'
											color:'gray'
										moment(i.date).format("dddd hh:mm")
									L.div className:'comm-text'
										i.text
					else ' '
			L.div
				className:'add-comm'
				React.createElement Form,
					onSubmit:@new_comment null
					className:'form'
					render: (api)->
						L.form
							style:
								width:'auto'
								margin:'8px'
							onSubmit:api.submitForm
							React.createElement Text,
								type:'text'
								field:'comment'
								placeholder:'comment'


export default Comments
	
