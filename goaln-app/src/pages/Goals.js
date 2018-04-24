import React, { Component } from 'react';
import Goal from '../modules/goal.js';
import config from '../config.js'
import axios from 'axios'


class Goals extends Component {

	state={
		id:config.def_id,
	}
	constructor (props) {
		super(props)
		console.log("ID",props)
		var id=props.id||props.match.params.id
		id= id||config.def_id

		console.log("ID",id)
		this.get_user_goals(id)
		//this.componentWillReceiveProps= this.componentWillReceiveProps.bind(this);

	}
	componentWillReceiveProps(props){
		var id=props.id||props.match.params.id
		console.log('new ID',id)
		this.get_user_goals(id)
	}
	get_user_goals(id){
		id= id||this.state.id
		console.log('getting goals');
		axios.get(config.server+'/usergoals/',
			{
				params:{id:id}
			},
		).then(g=> {
			console.log('got goas',g)
			this.setState({goals:g.data})
		})
	}

	render() {
		var goals="No goals yet"
		if (this.state.goals) {
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
