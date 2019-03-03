import React, { Component } from 'react'
import L from 'react-dom-factories'

export default class CounterPage extends Component
  constructor: ->
    super()
    @state =
      counter: 0

  _increment: (e) =>
    @setState
      counter: @state.counter + 1

  _decrement: (e) =>
    @setState
      counter: @state.counter - 1

  render: ->
    L.div null,
      L.h1 null, @state.counter
      L.h1 null, 'Hello world'
      L.button onClick: @_decrement, 'Decrement'
      L.button onClick: @_increment, 'Increment'

