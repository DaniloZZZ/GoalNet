import React, { Component } from 'react'
import L from 'react-dom-factories'
#import {Label} from '@smooth-ui/core-sc'
import { Form, Field } from 'react-final-form'
import axios from 'axios'
#import {debug_login} from '../../Utils/sessions.coffee'
L_ = React.createElement
import './login.less'

GNET_LOGIN=  'http://localhost:8919/login'

export default class LoginPage extends Component
  constructor: (props)->
    super(props)
    @state =
      counter: 0
    
  log_in:(form)=>
    #debug_login()
    data =
      email:form.email
      pwd:form.pwd
    console.debug 'making request', data
    axios.post GNET_LOGIN, data
      .then (response)=>
        console.log 'got response', response
        token = response.data.token
        @props.onLogin token
        window.location.reload()
  render: ->
    L.div className:'login page',
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

              L.button type:'submit','Login'
