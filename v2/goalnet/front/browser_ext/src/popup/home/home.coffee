
import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement
import './home.less'

export default class Page extends React.Component
  constructor:(props)->
    super(props)
    
  render: ->
    L.div className:'home',
      "Your activity is tracked"
