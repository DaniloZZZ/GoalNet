`
import React, { Component } from 'react'
import axios from 'axios'
import  './newgoal.css'
import { Form, Text, TextArea, Checkbox } from 'informed'
import DatePicker from 'react-datepicker'
import moment from 'moment'
import 'react-datepicker/dist/react-datepicker.css'
import Picker from '../modules/picker/picker.coffee'
`
import DOM from 'react-dom-factories'
import GoalNode from 'api/goal.coffee'
import UserNode from 'api/user.coffee'
User = new UserNode
Goal = new GoalNode

config= require(process.env.GOALNET_CONFIG_FILE)

log = console.log
{Component}= React
L_ = React.createElement
L = DOM

class Goals extends Component
	state:
		user_id:config.def_id
		sched:[]
		sched_new:[]
		goal:{}

	constructor: (props) ->
		super()
		log('props!',props)
		user_id=config.def_id||props.id
		@updateStatus = props.updateStatus
		User.get_goals(user_id).then (g)=>
			@setState goals:g
		User.get_sched(user_id).then( (scheds)=>
			for s in scheds
				log(s.parent)
				goals = @state.goals.filter(
					(g)->g._id==s.parent.item
				)
				log('goals fi',goals)
				s.goal_title = goals[0].title
			@setState sched:scheds
		).catch @onError(User)
	onError:(node)-> (err)->
		console.log(node.kind)
		console.error('Goals Component: Error->')
		node.onError(err)
		@updateStatus("Network error")

	achieveByChange: (date)=>
		@setState
			date: date
		console.log('date',@state.date)
	schedChange: (sch)=>
		log 'User added schedule',sch
		@setState
			sched:sch

	handleGoalChange:(formState)=>
		@setState(
			goal:formState.values
		)
	submitGoal:(e)=>
		data = @state.goal
		goal=Object.assign data,
				date:moment.now()
				user_id:@state.user_id
		log 'newgoal:',goal
		sched = @state.sched.filter (i)-> i.label=='new'
		console.log 'saving new goal with sched'
		Goal.create_with_schedule @state.user_id,goal,sched
			.then console.log

	render: ->
		L.div
			className:'newgoal'
			L_ Form,
				onChange:@handleGoalChange
				className:'form'
				L_ Text,
					field:"title"
					placeholder:'Goal Title'
				L_ TextArea, field:"desc",
					placeholder:'Description'
				L.label htmlFor:"share", 'Share'
				L_ Checkbox, field:"share", id:'share'
				L.div
					className:'datePicker'
					L.label null, 'Achieve by:'
					L_ DatePicker,
						selected:@state.date
						onChange:@achieveByChange
				L.button
					className:'btn', onClick:@submitGoal
					'Create'
			L_ Picker, schedule:@state.sched, onChange:@schedChange

export default Goals

