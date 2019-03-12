import React, { Component } from 'react'
import L from 'react-dom-factories'
import { BrowserRouter as Router, Route, Redirect, Link } from "react-router-dom"

import 'babel-polyfill'
L_ = React.createElement

##
export default Menu = ()->
  L.div className:'menu',
    L.div 0 ,
      L.div className:'menu-item',
        L_ Link, to:'/', 'home'
      L.div className:'menu-item',
        L_ Link, to:'/projects', 'Projects'
      L.div className:'menu-item',
        L_ Link, to:'/calendar', 'Calendar'
      L.div className:'menu-item',
        L_ Link, to:'/statistics', 'Statistics'
      L.div className:'menu-item',
        L_ Link, to:'/settings', 'Settings'
      L.div className:'menu-item',
        L_ Link, to:'/ADMIN', 'config_panel'




