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
			console.log('got goas',g)
			@setState goals:g
		@get_user_sched(id|| props.id)
		@handleDateChange =@handleDateChange.bind(@)

	get_user_goals: (id)->
		log 'getting goals'
		new Promise (res,rej)=>
			axios.get config.server+'/usergoals/',
				params:id:@state.id
			.then (g)=>res g.data
			.catch rej

	get_user_sched: (id)=>
		@get_user_goals(id)
		.then (goals)=>
			
		log 'getting goals'

	handleDateChange: (date)=>
		@setState
			date: date
		console.log('date',@state.date)

	submitForm:(date,id)=>
		return (data,e,api)=>
			log 'data',data
			log 'date',date
			axios.post(
				config.server+'/newgoal'
				Object.assign data,
					date:date
					id:id
			)

	render: ->
		L.div
			className:'newgoal'
			L_ Form,
				onSubmit: ()=>
					@submitForm @state.date,@state.id
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
			L_ Picker, schedule:@state.schedule
export default Goals
