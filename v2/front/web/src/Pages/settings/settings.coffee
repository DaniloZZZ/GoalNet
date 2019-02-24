
import React, { Component } from 'react'
import {Redirect, Link } from "react-router-dom"
import L from 'react-dom-factories'

L_ = React.createElement

export default class Page extends React.Component
  state:{}
  constructor:({uid})->
    super()
    @uid = uid
        
     
  render: ->
    console.log('rendering',this)
    L.div 0,
      L.div 0,
        L.div 0,
          L_ Link, to:'/', 'home'
        L.div 0,
          L_ Link, to:'/vkauth', 'auth vk'



