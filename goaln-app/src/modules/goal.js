import React, { Component } from 'react';
import axios from 'axios'
import './goal.css';

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
			this.state.title=this.props.data.title
		}
	}
	get_data(){
		console.log('getting goal');
		axios.get('http://localhost:3030/goals/',
				{
					params:{id:this.state.id}
				},
		).then(g=> {
			console.log('got goal',g)
			this.setState({title:g.data[0].title})
		})
		}
	render() {
    return (
      <div className="goal">
	  {this.state.title}
      </div>
    );
  }
}
export default Goal
