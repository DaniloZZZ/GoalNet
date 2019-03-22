import React, { Component } from 'react'
import L from 'react-dom-factories'
import {Label} from '@smooth-ui/core-sc'
import { Form, Field } from 'react-final-form'
import {debug_login} from '../../Utils/sessions.coffee'
L_ = React.createElement

export default class LoginPage extends Component
  constructor: ->
    super()
    @state =
      counter: 0
    
  log_in:()->
    debug_login()
    window.location.href='/'
  render: ->
    L.div className:'login page',
      L.h1 null, 'Login page'
      L_ Form,
        onSubmit:@log_in
        render: ({handleSubmit})->
          L.div className:'form',
            L.form onSubmit:handleSubmit,
              L.div 0,
                L.label 0, 'Email'
                L_ Field, name:'email',component:'input'
              L.div 0,
                L.label 0, 'Password'
                L_ Field, name:'pwd',type:'password',component:'input'

              L.button type:'submit','login'

