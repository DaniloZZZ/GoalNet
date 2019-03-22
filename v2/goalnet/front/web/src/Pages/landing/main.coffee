import React, { Component } from 'react'
import L from 'react-dom-factories'

import './landing.less'
import {Link } from "react-router-dom"

L_ = React.createElement

export default class Page extends Component
  constructor: ->
    super()
    @state =
      counter: 0
  render: ->
    L.div className:'landing',
      L.div className:'header',
        L.div className:'logo',
          'GoalNet'
        L.div className:'links',
          L_ Link, to:'/login','Log in'
      L.h1 null, 'Welcome to GoalNet'

