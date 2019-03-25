import React, { Component } from 'react'
import moment from 'moment'
import Chart from 'react-apexcharts'
import randomcolor from 'randomcolor'

import {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from 'recharts'
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
            type: 'chart'
            dataLabels:
                enabled:false
            xaxis:
                type:'datetime'
                categories:props.domain
            tooltip:
                x:
                    format:'hh:mm'
        if props.options
            @chartOpt = Object.assign {}, @chartOpt, props.options
        console.log 'Chart options', @chartOpt

    get_series_from_values:(values)->
        if not values
            return [0,0,0]
        return values

    render: ->
        series = @get_series_from_values(
            @props.values)

        console.log 'Graph: series',series
        console.log 'Graph: domain',@props.domain
        L.div className:'chart',
            L_ BarChart,
                data:@props.values
                height:600
                width:800
                L_ XAxis, dataKey:'time', tickFormatter:(timeStr) => moment(timeStr*1000).format('HH:mm')
                L_ YAxis
                L_ Legend
                for name,i in @props.domain or []
                  console.log 'name', name
                  L_ Bar, dataKey:name, key:i, stackId:'a', fill:randomcolor()
            L_ ParamPanel, onChanged:@onChange, params:@props.params

