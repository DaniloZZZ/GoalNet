import React, { Component } from 'react'
import L from 'react-dom-factories'
import Chart from 'react-apexcharts'
import moment from 'moment'

import { Index, timeSeries } from "pondjs"

import {Link } from "react-router-dom"
import Graph from '../graph/graph.coffee'
host = window.location.hostname

L_ = React.createElement

export default class Stat extends Component
  state:
    data:null
    params:
      'step minutes':80

  constructor: (props)->
    super(props)

  update_graph: (graphData)->
    console.log 'gradata', graphData
    data = []
    domain = []
    if graphData.data?
        # Get all occurent categories
        graphDataSeries = []
        for item in graphData.data
            for key in Object.keys(item)
                if key not in graphDataSeries
                    graphDataSeries.push key
        # aggregate values from array
        slice_key = (key, array)->
            res = []
            for elem in array
                res.push elem[key] || 0
            res
        # create series array
        data = []
        graphDataSeries = graphDataSeries.filter (e)->e!='time'
        for key in graphDataSeries
            data.push name:key, data:slice_key(key, graphData.data)
        domain = graphData.domain.slice(0,-1)
    graphOptions =
        type:'bar'
        chart:
            stacked:true
        dataLabels:
            enabled:false
        xaxis:
            categories:domain
    return options:graphOptions, data:data, names:graphDataSeries

  get_stats:({start,end,step})->
    axios.get API,
      params:
        user_id:@uid
        start:start
        end:end
        step:step

  render: ->
    {@options,@data,names} = @update_graph @props.data
    L.div className:'stats',
      "Web extension statistics"
      if @data
        L.div 0,
          L_ Graph,
            name:'websites visited'
            options:@options
            domain:names
            values:@props.data.data

      else
        L.p style:color:'#3C3C3C', "No stats yet"


