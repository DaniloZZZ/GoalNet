import React, { Component } from 'react'
import L from 'react-dom-factories'
import NewGoal from './new_goal.coffee'
import axios from 'axios'

L_ = React.createElement

host = window.location.hostname
API = 'http://'+host+':8991/'

export default class Page extends React.Component
  constructor:({uid})->
    super()
    console.log 'uid',uid
    @uid = uid
  create_task: (task)=>
    task.user_id = @uid
    console.log task
    axios.get API+'new_task',params:task
    .then (response)->
      res = response.data
      if res.split(':')[0]=='FAIL'
        console.log 'fail',res

  render: ->
    L.div 0,
      L_ NewGoal, onCreate:@create_task



