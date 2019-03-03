import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

export default class Pick extends React.Component
  state:
    value:0
  constructor:(props)->
    super(props)
    {label, value} = props
    @callback = props.onChange

  setValue:(val)->(e)=>
    @callback val

  change:(e)=>
    val = e.target.value
    val =Number(val)
    if val
      @callback e.target.value
  wheel:(e)=>
    delta = e.deltaY
    console.log 'dd',delta
    @callback @props.value + Math.sign(delta)

  focus: () =>
    @setState focus:true
  ufocus: () =>
    @setState focus:false
    
  render: ->
    {focus} = @state
    {label, value} = @props
    L.div className:'number',
      L.div className:'label', label
      L.div
        className:'edit'
        onMouseEnter:@focus
        onMouseLeave:@ufocus
        onWheel:@wheel
        L.div
          className:'pick '+(if focus then 'show' else 'hidden')
          for i in [3..-3]
            scale = i*Math.abs(i)/15 + 1
            v = scale*value
            if v==0
              v=i
            if v> 3
              v = Math.round(v)
            else
              v = Math.round(v*10)/10
            L.div
              className:'el'
              style:fontSize:parseInt(16-Math.abs(i))
              key:i
              onMouseDown:@setValue(v)
              v

        L.input
          type:'text'
          value:value
          onChange:@change
          onFocus:@focus
style:
  margin:2
  background:'#faa'
