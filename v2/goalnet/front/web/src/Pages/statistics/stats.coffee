
import React, { Component } from 'react'
import L from 'react-dom-factories'
import Chart from 'react-apexcharts'
import axios from 'axios'
import moment from 'moment'

import { Index, timeSeries } from "pondjs"
import VkOnline from '../../Modules/Vk/stats.coffee'

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

  constructor: ({uid})->
    super()
    @uid = uid

  render: ->
    L.div null,
      L.h1 null,'Stats'
      L.div 0,
        L_ VkOnline,uid:@uid,0


