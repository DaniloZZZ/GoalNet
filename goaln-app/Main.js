import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Goal from './modules/goal.js';
import axios from 'axios'
import ReactRouterDOM from 'react-router'
import Menu from './modules/menu.js'
import Users from './modules/users.js'

const {
	  HashRouter,
	  Switch,
	  Route,
	  Link
} = ReactRouterDOM

class App extends Component {
	constructor (props) {
		super()
		this.get_user_goals()
		this.get_user_info()
	}
	state={
		id:'5adcefbaed9d970d42d33d65',
		uinfo:{avatar:null,fname:'fa'},
	}

	get_user_info(id){
		console.log('getting user info');
		axios.get('http://localhost:3030/user/',
			{
				params:{id:id||this.state.id}
			},
		).then(g=> {
			console.log('got user info',g.data)
			this.setState({uinfo:g.data})
		})
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
			<div className="App">
				<p className="App-intro">
				</p>
				<div>
					<div>
						<p className='logo'>GoalNet</p>
					</div>
					<div className='uinfo'>
						<div className='uname-wrap'>
						<span className='uname'>
						{this.state.uinfo.fname}
					</span>
						</div>
							<img
								src={this.state.uinfo.avatar} 
								id='u' className="avatar"/>
					</div>
					<div className='main'>
					<Users></Users>
					<Menu> </Menu>
					</div>
				</div>
				<div className='goal-cont'>
					{goals}
				</div>
			</div>

		);
	}
}

export default App;
