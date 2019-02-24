import React, { Component } from 'react'
import Modal from 'react-responsive-modal';
import L from 'react-dom-factories'
L_ = React.createElement
import { Form, Field } from 'react-final-form'

export default class NewGoal extends React.Component
  state:
    open:false
  constructor:({onCreate})->
    super()
    @onCreate = onCreate

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
            onSubmit:@onCreate
            render:({handleSubmit})=>
              L.form onSubmit:handleSubmit,
                L.h2 0, "New goal"
                L.div 0,
                  L.label 0, "Name"
                  L_ Field, name:'name',component:'input',placeholder:'Name', null



