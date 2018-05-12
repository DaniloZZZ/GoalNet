React = require 'react'
ReactDOM = require 'react-dom'
moment = require 'moment'

import DOM from 'react-dom-factories'
import config from '../../config.js'
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

	get_user_data: (id) ->
		_=this

	new_comment: ->
		uid =  @state.uid
		gid =  @state.gid

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


export default Picker
	
