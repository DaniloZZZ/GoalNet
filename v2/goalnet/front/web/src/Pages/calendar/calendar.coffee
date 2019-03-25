import React, { Component } from 'react'
import L from 'react-dom-factories'
import Chart from 'react-apexcharts'
import axios from 'axios'
import moment from 'moment'

import { Index, timeSeries } from "pondjs"

import {Link } from "react-router-dom"
import BigCalendar from 'react-big-calendar'

API = 'http://localhost:8990/online'
L_ = React.createElement

export default class Page extends Component
  state:
    events:[
      {
        title:'foo'
        start:new Date(moment().subtract(1,'h'))
        end:new Date(moment())
      }

    ]

  constructor: ({uid})->
    super()
    console.log 'Rendering calendar page'
    @uid= uid
    console.log(@state.events)

  render: ->
    localizer = BigCalendar.momentLocalizer(moment)
    L.div null,
      L.h1 null, 'Calendar'
      L.div style:height:'600px',
        L_ BigCalendar,
          localizer:localizer
          events:@state.events
          startAccessor:'start'
          endAccessor:'end'


