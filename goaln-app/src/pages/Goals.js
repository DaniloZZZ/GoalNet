import React, { Component } from 'react';
import Goal from '../modules/goal.js';
import axios from 'axios'


class Goals extends Component {
	constructor (props) {
		super()
		var id='5adcefbaed9d970d42d33d65'
		this.get_user_goals(id|| props.id)
	}
	state={
		id:'5adcefbaed9d970d42d33d65',
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

	render() {
		var goals="No goals yet"
		if (this.state.goals) {
			console.log(this.state.goals)
			goals=this.state.goals.map(
				(e,i)=>{
					return (<Goal key={i} data={e}/>)
				})
		}
		return (
			<div className='goal-cont'>
				{goals}
			</div>

		);
	}
}

export default Goals;
