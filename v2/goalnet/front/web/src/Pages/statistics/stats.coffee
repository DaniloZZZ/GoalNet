
import React, { Component } from 'react'
import L from 'react-dom-factories'
import Chart from 'react-apexcharts'
import axios from 'axios'
import moment from 'moment'

import { Index, timeSeries } from "pondjs"
import VkOnline from '../../Modules/stats/vk.coffee'
import WebExt from '../../Modules/stats/webext.coffee'

import {Link } from "react-router-dom"
host = window.location.hostname
API = 'http://'+host+':8990/online'

L_ = React.createElement
zip = (arrays)->
    arrays[0].map (_,i)->
        return arrays.map (array)->array[i]

export default class Page extends Component
  state:
    data:null
    integral:{}

  constructor: (props)->
    super(props)
    {@uid, @api} = props
    @api.add_trigger 'webext.metrics', (metrics)=>
      console.log 'tr', metrics
      if metrics.name=='integral'
        @setState integral:metrics
    end = moment()
    start = moment().subtract 1, 'hours'
    console.log 'emd', end
    @api.get_integral_metrics
      name:'websites'
      start:start.unix()
      end:end.unix()

  render: ->
    L.div null,
      L.h2 null,'Statistics'
      L.div 0,
        L_ WebExt, data:@state.integral


