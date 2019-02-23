import React, { Component } from 'react'
import L from 'react-dom-factories'
import { BrowserRouter as Router, Route, Link } from "react-router-dom"

import LoginPage from './Pages/login/login.coffee'
L_ = React.createElement

export default App= ->
    L_ Router, null,
      L.div 0,
        L.li 0,
          L.ul null,
            L_ Link, to:'/', "Home"
          L.ul null,
            L_ Link, to:'/login', "Log in"
        L_ Route,
          exact: true
          path:'/'
          component: HomePage
        L_ Route,
          path:'/login'
          component:LoginPage

HomePage = ()->
  L.div 0,
    'Home'
    L.h2 0, "This is a home page"


