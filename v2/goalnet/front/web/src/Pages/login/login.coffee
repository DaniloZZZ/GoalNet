import React, { Component } from 'react'
import L from 'react-dom-factories'
import {debug_login} from '../../Utils/sessions.coffee'

export default class LoginPage extends Component
  constructor: ->
    super()
    @state =
      counter: 0
    
  log_in:->
    debug_login()
    window.location.href='/'
  render: ->
    L.div null,
      L.h1 null, 'Login page'
      L.button onClick:@log_in, 'login'

