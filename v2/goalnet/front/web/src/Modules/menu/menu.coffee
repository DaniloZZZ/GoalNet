import React, { Component } from 'react'
import L from 'react-dom-factories'
import { BrowserRouter as Router, Route, Redirect, Link } from "react-router-dom"
import {log_out} from '../../Utils/sessions.coffee'

import 'babel-polyfill'
L_ = React.createElement

##
export default Menu = ()->
  onlog_out=->
    log_out()
    window.location.reload()
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
      L.button onClick:onlog_out, 'log out'




