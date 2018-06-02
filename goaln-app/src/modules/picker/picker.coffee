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
		super(props)
		momd = (i)=>moment().days(i)
		sch = props.schedule || (date:momd(i),items:[],id:i for i in [1,2,3,4,5,6,7])
		dates=(momd(i) for i in [1,2,3,4,5,6,7])
		@state =
			dates:dates
			children:[]
			schedule:sch

	itemCreate: (date)=>(item)=>
		l 'new item',item
		sch = @state.schedule.map (s)=>
			if s.date==date
				item.id = (s.items||[]).length+1
				item.label='new'
				l item,s.items
				s.items.push(item)
			return s
		l 'item created, sch is', sch
		# need to convert from local obj, sorted by day to 
		# unified architecture [{start:Date,end:Date},..]
		itemArr=sch.map (ch)->ch.items
		unif_sch=[].concat itemArr...
		l sch, unif_sch
		@props.onChange(unif_sch)

	@getDerivedStateFromProps: (props,state)->
		# Converting from list of items to children of every day
		if not props.schedule
			return state
		sch = props.schedule
		l 'state der', state,sch
		sch_new= []
		n=0
		for date in state.dates
			do(date)->
				n=n+1
				this_day=sch.filter (i)->
					moment(i.start).day()==date.day()
				sch_new.push
					date:date
					items:this_day
					id:date.day()
		l sch,sch_new
		Object.assign state, schedule:sch_new

	render: ->
		canvs=for day in @state.schedule
			do (day)=>
				L_ Canvas,
					date:day.date
					id:day.id
					children:day.items
					onItemCreate:@itemCreate(day.date)
		L.div
			className:'picker'
			style:
				backgroundColor:'#fff0ed'
				position:'relative'
				borderRadius:'0.3em'
				display:'flex'

			L.div
				style:
					width:'auto'
				canvs...

export default Picker
	
