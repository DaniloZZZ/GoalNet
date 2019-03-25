import React, { Component } from 'react'
import {Route, Redirect, Link } from "react-router-dom"
import L from 'react-dom-factories'

L_ = React.createElement

export default menu = (props)->
  l = window.location.pathname
  L.div className:"settings-menu",
    L_ Link, to:'connectors', "Connectors"
    L_ Link, to:'#profile', "Profile"
          
     
