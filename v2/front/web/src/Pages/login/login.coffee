import React, { Component } from 'react'
import L from 'react-dom-factories'

export default class LoginPage extends Component
  constructor: ->
    super()
    @state =
      counter: 0
  render: ->
    L.div null,
      L.h1 null, 'Login page'

