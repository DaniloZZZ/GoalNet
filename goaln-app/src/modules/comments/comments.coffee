React = require 'react'
ReactDOM = require 'react-dom'
moment = require 'moment'
import DOM from 'react-dom-factories'
import config from '../../config.js'
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

	new_comment: ->
		uid =  @state.uid
		gid =  @state.gid
		(data) ->
			l data, id
		axios.post
				config.server+'/comment/'
				Object.assign
					act:'add'
					id:gid
					uid:uid
					text:data.comment
					date:moment()


		).then(g=> {
			console.log('got user info',g.data)
			this.setState({uinfo:g.data})
		})



	render: ->
		L.div
			className:'comments'
			L.div
				className:'comms'
					if @state.comm
						@state.comm.map (i)->
							L.div
									className:'comm'
									i.text
					else 'no comments yet '
			L.div
				className:'add-comm'
				React.createElement Form,
					onSubmit:@new_comment null
					className:'form'
					render: (api)->
						L.form
							onSubmit:api.submitForm
							React.createElement Text,
								type:'text'
								field:'comment'
								placeholder:'comment'


export default Comments
	
