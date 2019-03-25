
import React, { Component } from 'react'
import {BrowserRouter, Route, Redirect, Link } from "react-router-dom"
import {Switch} from '@smooth-ui/core-sc'
import Menu from './menu.coffee'
import GnetAPI from '../../Utils/gnetAPI/gnetAPI.coffee'
import './settings.less'
import L from 'react-dom-factories'

L_ = React.createElement

export default class Page extends React.Component
  state:
    connectors:[]
  extStatus:null
  constructor:(props)->
    super(props)
    {uid, api, route} = props
    @uid = uid
    @api = api
    @match = route.match
    api?.get_integral_metrics 'foo'
    api?.get_connectors (conn)=>
      if not conn.modules?
        console.log 'Wrong response', conn
      conn = conn.modules
      console.info 'connectors are', conn
      @setState connectors: conn
  toggleExt:(swit)=>
    console.log 'Toggle extension'
    if 'webext' not in @state.connectors
      @api.add_connector 'webext'
      @api.add_record 'websites'

     
  render: ->
    console.log('rendering settings page',this)
    L_ BrowserRouter, basename:'settings',
      L.div className:'page',
        L.h2 0, "Settings"
        L_ Menu
        L.div className:'settings',
          L_ Route,
            exact: true
            path: '/connectors'
            render:()=>
              console.log 'rencon'
              L.div className:'pane',
                L.div className:'setting',
                  L.div className:'title', 'Browser extension'
                  L.div className:'body',
                    L.div className:'option',
                      L.label 0,"Enabled"
                      L.div className:'input',
                        L_ Switch, onChange:@toggleExt,checked:'webext' in @state.connectors, labeled:true

                L.div className:'setting',
                  L.div className:'title', 'VK bot and tracker'
                  L.div className:'body',
                    L.div className:'option',
                      L.label 0,"Connect"
                      L.div className:'input',
                        L_ Link, to:'/vkauth', 'Authorise in VK'



