# React + Coffeescript = Web Extension

technologies included:

 - coffeescript
 - less, css



Browsers:
    - Firefox >48
    - Chrome

HMR is currently not set up
use web-ext from firefox to hot-reload on filechange


# Why coffeescript?

because it's less verbose. I personally love to use this style of syntax:

```coffeescript
import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

Greeting = ()->
  L.div className:'greeting',
	L.h2 style:textAlign:'center', 'Hello World'

export default class App extends React.Component
  constructor:->
    super()
     
  render: ->
    L.div className:'app',
      L_ Greeting, null

ReactDOM.render <App />, document.getElementById 'root'

```
