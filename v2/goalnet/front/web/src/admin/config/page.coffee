
import React, { Component } from 'react'
import {JsonTree} from 'react-editable-json-tree'
import L from 'react-dom-factories'
import { Form, Field } from 'react-final-form'
import ConnectionWidget from '../../Utils/websockets/connection_widget.coffee'
import NotificationWidget from '../../Modules/notifications/widget.coffee'
import JsonBeauty from '../../Modules/json_beauty/JsonBeauty.coffee'
import {Connector} from '../../Utils/websockets/connector.coffee'
import Graph from '../../Modules/graph/graph.coffee'
import './admin.less'
L_ = React.createElement

get_api_path = ->
    """
    Gets the api for websockets server
    """
    host = window.location.hostname
    port = 3032
    api_path = 'ws://'+ host+':'+port
    api_path

export default class Page extends React.Component
    state:
      notifs:[]
      action_data:
        user_id:1
      graphData: []
    constructor:(props)->
      super(props)
      api_path = get_api_path()
      console.log 'apipath',props.api
      @connector = props.api
      @connector.add_callback @onNotif

    onNotif:(notif)=>
      @setState (s,p)->
        s.notifs.unshift notif
        if notif.data?
          s.graphData = notif
        s

    send:(form)=>
      form = @state.action_data.a
      console.log 'Sending', form
      @connector.send(JSON.stringify(form))
    formUpdate:(data)=>
      @setState action_data:data

    render: ->
        capitalize = (s) -> s[0].toUpperCase() + s.slice(1)
        {graphData, action_data} = @state
        data = []
        domain = []
        if graphData.data?
            # Get all occurent categories
            graphDataSeries = []
            for item in graphData.data
                for key in Object.keys(item)
                    if key not in graphDataSeries
                        graphDataSeries.push key
            # aggregate values from array
            slice_key = (key, array)->
                res = []
                for elem in array
                    res.push elem[key] || 0
                res
            # create series array
            data = []
            for key in graphDataSeries
                if key != 'time'
                    data.push name:key, data:slice_key(key, graphData.data)
            domain = graphData.domain.slice(0,-1)
        console.log 'grapn data', data
        console.log 'grapn domain', domain
        graphOptions =
            type:'bar'
            chart:
                stacked:true
            dataLabels:
                enabled:false
            xaxis:
                categories:domain
            
        field = (key, value)->
            L.div 0,
                L.label 0,capitalize(key)
                L_ Field, name:key, component:'input', value:value
        L.div 0,
            L.h2 0, "Admin panel for GoalNet"
            L_ ConnectionWidget, connector:@connector
            L_ NotificationWidget, notifs:@state.notifs
            L.div class:'send-action form',
                L_ Form,
                        onSubmit:@send
                        render:({handleSubmit})->
                                L.form onSubmit:handleSubmit,
                                        L.h2 0, "Compose a message"
                                                field 'type'
                                                field 'app'
                                                for k,v of action_data
                                                    field k,v
                                        L.button type:'submit', 'Send'
            L.div style:textAlign:'left',
                L_ JsonTree, data:action_data, onFullyUpdate:@formUpdate
            L.div className:"admin-graph",
                L_ Graph, options:graphOptions, values:data, domain:domain
                            

