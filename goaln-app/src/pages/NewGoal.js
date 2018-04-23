import React, { Component } from 'react';
import axios from 'axios'
import  './newgoal.css'
import { Form, Text, TextArea, Checkbox } from 'react-form';
import DatePicker from 'react-datepicker';
import moment from 'moment';
import 'react-datepicker/dist/react-datepicker.css';




class Goals extends Component {
	state={
		id:'5adcefbaed9d970d42d33d65',
		date:moment(),
	}
	constructor (props) {
		super()
		var id='5adcefbaed9d970d42d33d65'
		this.get_user_goals(id|| props.id)
		this.handleDateChange = this.handleDateChange.bind(this);
	}

	get_user_goals(id){
		console.log('getting goals');
		axios.get('http://localhost:3030/usergoals/',
			{
				params:{id:this.state.id}
			},
		).then(g=> {
			console.log('got goas',g)
			this.setState({goals:g.data})
		})
	}
	handleDateChange(date) {
		this.setState({
			date: date
		});
		console.log('date',this.state.date)
	}
	submitForm(date,id){
		return function(data,e,api){
			console.log('data',data)
			console.log('date',date)
			axios.post(
				'http://localhost:3030/newgoal',
				Object.assign(data,{
					date:date,
					id:id})
			)
		}
	}
	render() {
		return (<Form onSubmit={
			this.submitForm(
				this.state.date,
				this.state.id)} className='form' render={(
    api
  ) => {
	  return(
    <form onSubmit={api.submitForm}>
      <Text field="title" placeholder='Goal Title' />
      <TextArea field="desc"  placeholder='Description'/>

      <Checkbox field="share" id='share'/>
	  <label htmlFor="share">Share</label>
	  <div className='datePicker'>
		  <label> Achieve by:</label>
	  <DatePicker  
		  selected={this.state.date}
		  onChange={this.handleDateChange}></DatePicker>
  </div>
	  <button className='btn' type="submit">Create</button>
    </form>
	  )}
  } />
  )
	}
}

export default Goals;
