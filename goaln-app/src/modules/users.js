import React, { Component } from 'react';
import axios from 'axios'
import './users.css';


class Users extends Component {
	constructor (props) {
		super()
		this.get_users()
	}
	state={
		id:'5adcefbaed9d970d42d33d65',
	}

	get_users(id){
		console.log('getting users');
		axios.get('http://localhost:3030/users/',
			{
				params:{id:this.state.id}
			},
		).then(g=> {
			console.log('got users',g)
			this.setState({users:g.data})
		})
	}
	render() {
		var users="No users yet"
		if (this.state.users) {
			console.log(this.state.users)
			users=this.state.users.map(
				(e,i)=>
				{return (
					<div>
						<a key={i} href={"users/"+e._id}>
							<img
								src={e.avatar} 
								alt={"view"+e.fname+"'s goals"}
								className="avatar"/>
							<div className='name'>{e.fname}
							</div>
						</a>
					</div>
				)
				})
		}

		return (
			<div className="users">
					{users}
			</div>

		);
	}
}

export default Users;
