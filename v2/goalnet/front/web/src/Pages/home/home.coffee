import React, { Component } from 'react'
import L from 'react-dom-factories'
import Chart from 'react-apexcharts'
import Graph from '../../Modules/graph/graph.coffee'


L_ = React.createElement

export default class HomePage extends Component
  constructor: ({uid})->
    super()
    @uid= uid

  render: ->
    L.div null,
      L.h1 null, 'Welcome'
      L_ Graph,0,0
