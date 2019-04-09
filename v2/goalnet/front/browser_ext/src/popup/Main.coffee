import React, { Component } from 'react'
import L from 'react-dom-factories'
#import LoginPage from '../../../web/src/Pages/login/login.coffee'
import LoginPage from './login/login.coffee'
import HomePage from './home/home.coffee'
import {get_status,get_session, save_session} from './session/sess.coffee'
L_ = React.createElement

if chrome
  browser=chrome

sendTest = ()->
  console.log('sending')
  browser.runtime.sendMessage
    action:'test'
    message:'fooar'

export default class Popup extends React.Component
  state:
    session:null
    waiting:true
    status:'Loading...'
  constructor:(props)->
    super(props)
    console.log 'Popup props', props
    get_session()
      .then (session)=>
        @setState session:session, waiting:false

    get_status()
      .then (status)=>
        @setState status:status

  onLogin:(token)->
    save_session token
  render: ->
    {session, waiting} = @state
    console.log 'Rendering popup with session', session
    L.div className:"Popup",
      if @error
        "Error"+ @error
      if waiting
        "Loading..."
      else
        if not session.session?.token
          L_ LoginPage, onLogin:@onLogin
        else
          L_ HomePage
        
        L.div className:'button',height:50,onClick:sendTest,'click'
        L.div className:'status',@state.status

