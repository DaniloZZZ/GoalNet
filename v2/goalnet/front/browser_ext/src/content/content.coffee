import React, { Component } from 'react'
import L from 'react-dom-factories'
import ReactDOM from 'react-dom'
L_ = React.createElement
if chrome
  browser=chrome

console.log 'hello content!'
body =document.getElementsByTagName('body')[0]

onEvent = (event_type)->(e)->
  console.log event_type,'event'
  browser.runtime.sendMessage
    event_type: event_type
    action:'post.event'
    (response) ->
      console.log('resp',response.farewell)
      
event_types = ['mousemove','click','scroll']

for event in event_types
  window.addEventListener( event, onEvent event)

root = document.createElement("div")
root.id='root'
body.appendChild(root)

Main = (props)->
  L.div
    className:'extover'
    style:
      position:'fixed'
      backgroundColor:'#0A4B9A60'
      bottom:40
      right:300
      borderRadius:3
      fontFamily:'monospace'
      fontWeight:'bold'
      color:'#BF2D9F'
      padding:'1em'
    "Hello content"

ReactDOM.render <Main />, root
