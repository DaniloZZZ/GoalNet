import React, { Component } from 'react'
import L from 'react-dom-factories'
import Chart from 'react-apexcharts'
import axios from 'axios'
import moment from 'moment'

import { Index, timeSeries } from "pondjs"

import {Link } from "react-router-dom"
import Graph from '../graph/graph.coffee'
host = window.location.hostname
API = 'http://'+host+':8990/online'

L_ = React.createElement

export default class VkOnline extends Component
  state:
    data:null
    params:
      'step minutes':80

  constructor: ({uid})->
    super()
    @uid= uid
    @update_graph(@state.params['step minutes'])

  update_graph: (step)->
    now = Date.now()/1000
    props =
      start:now-60*60*16
      end:now
      step:step*60 || 900
    ts = (moment.unix(num).format("ddd, h:mm") for num in [props.start..props.end] by props.step)
    ts = (num*1000 for num in [props.start..props.end] by props.step)
    domain = ts
    @get_stats( props )
    .then (response)=>
      data = response.data
      data = (moment.duration(sec,'seconds').minutes() for sec in data)
      console.log(data)
      @setState values:data,domain:domain

  onParams:(update)=>
    @update_graph(update['step minutes'])
    @setState (s,p)->
      s.params = Object.assign s.params,update
      s

  get_stats:({start,end,step})->
    axios.get API,
      params:
        user_id:@uid
        start:start
        end:end
        step:step

  render: ->
    L.div null,
      if @state.values
        L.div 0,
          L_ Graph,
            name:'vk online'
            params:@state.params
            onParamsChange:@onParams
            domain:@state.domain
            values:@state.values

      else
        L.h2 0, "No stats yet"


