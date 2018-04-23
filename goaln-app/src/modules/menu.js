import React, { Component } from 'react';

import {Link} from 'react-router-dom'
import './menu.css';



class Menu extends Component {
	constructor (props) {
		super(props)
		this.menuItems=[{
			name:'My goals',
			link:'home',
		},
		{
			name:'Explore',
			link:'explore'
		},
		{
			name:'Create a goal',
			link:'newgoal'
		},
		{
			name:'Statistics',
			link:'stats'
		},
		]
	}
  render() {
	  var items=this.menuItems.map(i=>{
		  return (<div className="menu-item">
				  <Link to={i.link}>{i.name}</Link>
				  </div>)
	  })
    return (
      <div className="menu">
		<p>Menu</p>
	  <div id="item1">
	  {items}
	  </div>
      </div>

    );
  }
}

export default Menu
