import React, { Component } from 'react'
import L from 'react-dom-factories'

import {Link } from "react-router-dom"

L_ = React.createElement

export default class VkAuthPage extends Component
  constructor: ->
    super()
    @state =
      counter: 0
  render: ->
    L.div null,
      L.h1 null, 'Welcome'
      L_ Link, to:'/login','Log in'

