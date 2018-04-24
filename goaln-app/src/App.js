import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'
import {Switch, Route} from 'react-router-dom'
import config from './config.js'

import Menu from './modules/menu.js'
import Users from './modules/users.js'
import Goals from './pages/Goals.js'
import NewGoal from './pages/NewGoal.js'

class App extends Component {
	constructor (props) {
		super()
		this.get_user_info()
	}
	state={
		id:config.def_id,
		uinfo:{avatar:null,fname:'fa'},
	}

	get_user_info(id){
		console.log('getting user info');
		axios.get(config.server+'/user/',
			{
				params:{id:id||this.state.id}
			},
		).then(g=> {
			console.log('got user info',g.data)
			this.setState({uinfo:g.data})
		})
	}
	render() {
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
			<Users></Users>
			<Menu> </Menu>
		<div className='main'>
			<Switch>
				<Route path='/home' component={Goals}/>
				<Route path='/newgoal' component={NewGoal}>
				</Route>
				<Route path='/user/:id' component={Goals}/>
				<Route path='/user/'>
					user
				</Route>
			</Switch>
		</div>
		</div>
	</div>

		);
	}
}

export default App;
