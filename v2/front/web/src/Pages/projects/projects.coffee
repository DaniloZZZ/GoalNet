import React, { Component } from 'react'
import L from 'react-dom-factories'
import NewGoal from './new_goal.coffee'


L_ = React.createElement

export default class Page extends React.Component
  constructor:({uid})->
    super()
    @uid = uid
  create_task: (task)->
    console.log task
  render: ->
    L.div 0,
      L_ NewGoal, onCreate:@create_task





