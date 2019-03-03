import React, { Component } from 'react'
import Modal from 'react-responsive-modal'
import L from 'react-dom-factories'
import Timekeeper from 'react-timekeeper'
import moment from 'moment'
L_ = React.createElement
import { Form, Field } from 'react-final-form'

export default class NewGoal extends React.Component
  state:
    open:false
  constructor:({onCreate})->
    super()
    @onCreate = onCreate

  onCreateTask:(task)=>
    task.start=moment(@state.start).unix()
    task.end=moment(@state.end).unix()
    @onCreate(task)
    @onClose()

  changeStart:(ts)=>
    @setState start:ts.formatted
  changeEnd:(ts)=>
    @setState end:ts.formatted
  onOpen:=>
    @setState open:true
  onClose:=>
    @setState open:false

  render: ->
    {open} = @state
    L.div 0,
      L.button onClick:@onOpen, "New Task"
      L_ Modal, open:open, onClose:@onClose, center:true,
        L.div 0,
          L_ Form,
            onSubmit:@onCreateTask
            render:({handleSubmit})=>
              L.form onSubmit:handleSubmit,
                L.h2 0, "New goal"
                L.div 0,
                  L.label 0, "Name"
                  L_ Field, name:'name',component:'input',placeholder:'Name', null
                  L.div style:width:700,
                    L.div style:float:'left',
                      L.h3 0, "Start:"
                      L_ Timekeeper, time:@state.start,onChange:@changeStart
                    L.div style:float:'right',
                      L.h3 0, "End:"
                      L_ Timekeeper, time:@state.end,onChange:@changeEnd
                    L.button type:'submit', 'Create'



