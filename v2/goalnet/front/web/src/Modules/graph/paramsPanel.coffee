
import React, { Component } from 'react'
import L from 'react-dom-factories'
import Number from './numberPick.coffee'
L_ = React.createElement

export default class Panel extends React.Component
  constructor:(props)->
    super(props)
    @onChanged = props.onChanged

  handler: (label)->(value)=>
    @onChanged [label]:value

  render: ->
    {params} = @props
    if not params
      return null
    L.div className:'param-panel',
      for own label, value of params
        console.log 's',label
        L_ Number,
          key:label
          label:label
          value:value
          onChange:@handler(label)

