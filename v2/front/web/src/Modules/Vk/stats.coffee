import React, { Component } from 'react'
import L from 'react-dom-factories'
import Chart from 'react-apexcharts'
import axios from 'axios'
import moment from 'moment'

import { Index, timeSeries } from "pondjs"

import {Link } from "react-router-dom"
host = window.location.hostname
API = 'http://'+host+':8990/online'

L_ = React.createElement

export default class VkOnline extends Component
  state:
    data:null

  constructor: ({uid})->
    super()
    @uid= uid
    now = Date.now()/1000
    props =
      start:now-60*60*12
      end:now
      step:900
    ts = (moment.unix(num).format("ddd, h:mm") for num in [props.start..props.end] by props.step)
    console.log(ts)
    @chartOpt=
      chart:
        id: 'apexchart-example'
      dataLabels:
        enabled:false
      xaxis:
        categories: ts

    @get_stats( props )
    .then (response)=>
      data = response.data
      data = (moment.duration(sec,'seconds').minutes() for sec in data)
      console.log(data)
      @setState data:[{name:'vkonline',data:data}]

  get_stats:({start,end,step})->
    axios.get API,
      params:
        user_id:@uid
        start:start
        end:end
        step:step

  render: ->
    L.div null,
      if @state.data
        L.div 0,
          L_ Chart, options:@chartOpt,series:@state.data, type:'area',height:500
      else
        L.h2 0, "No stats yet"


