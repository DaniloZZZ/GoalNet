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
		L.div className:'chart',
			L_ Chart,
				options:@props.options
				series:series
				type:@chartOpt.type
				height:500
			L_ ParamPanel, onChanged:@onChange, params:@props.params

