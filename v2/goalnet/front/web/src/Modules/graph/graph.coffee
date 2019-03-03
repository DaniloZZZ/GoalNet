import React, { Component } from 'react'
import moment from 'moment'
import Chart from 'react-apexcharts'
import L from 'react-dom-factories'
import './graph.less'
import ParamPanel from './paramsPanel.coffee'
L_ = React.createElement

export default class Graph extends React.Component
  constructor:(props)->
    super(props)
    @onChange=props.onParamsChange
    console.log('d',props.domain)
    @chartOpt=
      chart:
        id: 'chart'
      dataLabels:
        enabled:false
      xaxis:
        type:'datetime'
        categories:props.domain
      tooltip:
        x:
          format:'hh:mm'

  render: ->
    series= [{name:@props.name,data:@props.values}]
    if @chartOpt.xaxis.type=='datetime'
      data = []
      for v ,i in @props.values
        data.push
          x:@props.domain[i]
          y:v
        series =[ data:data] 

    console.log 'dafsd',series
    L.div className:'chart',
      L_ Chart,
        options:@chartOpt
        series:series
        type:'area'
        height:500
      L_ ParamPanel, onChanged:@onChange, params:@props.params

