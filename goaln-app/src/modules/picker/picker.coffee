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
		momd = (i)=>moment().days(i)
		@days = (date:momd(i),items:[],id:i for i in [1,2,3,4,5,6,7])
		l @days
		@state =
			dates:[]
			children:[]
			sched:@days
	get_user_data: (id) ->
		_=this

	new_comment: ->
		uid =  @state.uid
		gid =  @state.gid

	itemCreate: (date)=>(item)=>
		l 'new item',item
		sch = @state.sched.map (s)=>
			if s.date==date
				l s
				s.items.push(item)
			else
				s.items
		@setState
			children:sch

	render: ->
		canvs=for day in @state.sched
			do (day)=>
				L_ Canvas,
					date:day.date.format('dddd')
					id:day.id
					children:day.items
					onItemCreate:@itemCreate(day.date)
		L.div
			className:'picker'
			style:
				backgroundColor:'blue'
				position:'relative'
				borderRadius:'0.3em'
				display:'flex'

			L.div
				style:
					width:'auto'
				canvs...

export default Picker
	
