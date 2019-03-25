import React, { Component } from 'react'
import L from 'react-dom-factories'
#import LoginPage from '../../../web/src/Pages/login/login.coffee'
import LoginPage from './login/login.coffee'
import HomePage from './home/home.coffee'
import {get_session, save_session} from './session/sess.coffee'
L_ = React.createElement

export default class Popup extends React.Component
  state:
    session:null
    waiting:true
  constructor:(props)->
    super(props)
    console.log 'Popup props', props
    get_session()
      .then (session)=>
        @setState session:session, waiting:false

  onLogin:(token)->
    save_session token
  render: ->
    {session, waiting} = @state
    console.log 'sess ren', session
    L.div className:"Popup",
      if waiting
        "Loading..."
      else
        if not session.session?.token
          L_ LoginPage, onLogin:@onLogin
        else
          L_ HomePage

