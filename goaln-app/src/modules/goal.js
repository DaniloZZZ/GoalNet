import React, { Component } from 'react';
import axios from 'axios'
import ReactHover from 'react-hover'
import Comments from './comments/comments.coffee'

import './goal.css';

var config= require(process.env.GOALNET_CONFIG_FILE)

class Goal extends Component {
	constructor (props) {
		super(props)
		this.state = {
			id:props.id,
			title: 'No title',
		};
		console.log('propss',props)
		if (!this.props.data){
			this.get_data()
		}
		else{
			var goal = this.props.data
			this.state = Object.assign(this.state,goal)
		}
	}
	componentWillReceiveProps(props){
		var goal = props.data
		this.setState(goal
		)
	}

	get_data(){
		console.log('getting goal');
		axios.get('http://localhost:3030/goals/',
			{
				params:{id:this.state.id}
			},
		).then(g=> {
			console.log('got goal',g)
			var goal =g.data[0]
			this.setState(goal)
		})
	}
	
	deleteGoal(id){
		return function(){
		console.log('deleting  goal');
		axios.get(config.server+'/donegoal/',
			{
				params:{id:id}
			},
		).then(g=> {
			console.log('got goal',g)
		})
		}
	}

	render() {
		var done = false
		 if (this.state.done){
			done="done"
		}
		return (
			<div>
			<div className={"goal "+done }>
						<div className='goal-title'>
							{this.state.title}
						</div>
						<div className='goal-desc'>
							{this.state.desc}
						</div>
						<div className='goal-hover'>
							<div class='goal-del' onClick={this.deleteGoal(this.state._id)}>
								<img className='goal-img' src="https://image.flaticon.com/icons/png/512/61/61685.png"/>
							</div>
						</div>
			</div>
			<Comments gid={this.state._id} comments={this.state.comments}/>
			</div>
		);
	}
}

export default Goal
