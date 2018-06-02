`
import React, { Component } from 'react'
import axios from 'axios'
import  './newgoal.css'
import { Form, Text, TextArea, Checkbox } from 'react-form'
import DatePicker from 'react-datepicker'
import moment from 'moment'
import 'react-datepicker/dist/react-datepicker.css'
import Picker from '../modules/picker/picker.coffee'
import DOM from 'react-dom-factories'
`
config= require(process.env.GOALNET_CONFIG_FILE)

log = console.log
{Component}= React
L_ = React.createElement
L = DOM

class Goals extends Component
	state:
		id:config.def_id
		date:moment()

	constructor: (props) ->
		super()
		id=config.def_id
		@get_user_goals(id|| props.id)
		.then (g)=>
			@get_user_sched g
			@setState goals:g
		@handleDateChange =@handleDateChange.bind(@)

	get_user_goals: (id)->
		log 'getting goals'
		new Promise (res,rej)=>
			axios.get config.server+'/usergoals/',
				params:id:@state.id
			.then (g)=>res g.data
			.catch rej

	get_user_sched: (goals)=>
		momd = (i)=>moment().days(i)
		# goals is [{ goal:'foo',sched:[{start:'121',id:'adf'},{...}]},...]
		# Making array of items
		# {start:,end:,name:goalname}
		makeItemArr=(goal)->
			(Object.assign item,name:goal.title for item in goal.sched)
		arrays=goals.map makeItemArr
		items=[].concat arrays...
		@setState schedule:items

	handleDateChange: (date)=>
		@setState
			date: date
		console.log('date',@state.date)
	schedChange: (sch)=>
		log 'page sched change',sch
		log 'setting state'
		@setState
			schedule:sch

	submitForm:(date,id)=>
		return (data,e,api)=>
			goal=Object.assign data,
					date:date
					sched: @state.schedule.filter (i)-> i.label=='new'
					id:id
			log 'newgoal:',goal
			axios.post(
				config.server+'/newgoal',goal
			)

	render: ->
		L.div
			className:'newgoal'
			L_ Form,
				onSubmit:@submitForm @state.date,@state.id
				className:'form'
				render:(api)=>
					L.form
						onSubmit:api.submitForm
						L_ Text,
							field:"title"
							placeholder:'Goal Title'
						L_ TextArea, field:"desc",
							placeholder:'Description'
						L_ Checkbox, field:"share", id:'share'
						L.label htmlFor:"share", 'Share'
						L.div className:'datePicker'
							L.label null, 'Achieve by:'
							L_ DatePicker,
								selected:@state.date
								onChange:@handleDateChange
						L.button className:'btn', type:'submit',
							'Create'
			L_ Picker, schedule:@state.schedule, onChange:@schedChange

export default Goals

