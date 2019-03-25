import React, { Component } from 'react'
import L from 'react-dom-factories'
import style from './connection.less'

L_ = React.createElement

export default class Widget extends React.Component
    state :
        connected:false
        waiting:false
        path: 'ws://localhost:3032'
        error:""
        addr:""

    constructor:(props)->
        super(props)
        {connector} = props
        if connector
            connector.setOnStateChange(@onConnectorStateChange)
            @connector = connector
        else
            @state.error='No connector provded to widget'
        @state.path = @connector.api_path
        @state.connected = @connector.connected

    onConnectorStateChange:(state_id, event)=>
        switch state_id
            when 'open' then @onOpenedConn()
            when 'error' then @onError(event)
            when 'closed' then @onClose()

    doAction:(e)=>
        status = @getStatus()
        switch status
            when 'connected' then @disconnect()
            when 'error' then @reconnect()
            when 'disconnected' then @reconnect()

    getStatus:()->
        {connected, error, waiting} = @state
        console.log 'Current connection status', connected
        status = if connected then 'connected' else 'disconnected'
        if waiting
            status = 'waiting'
        if error
            status = 'error'
        console.log 'Next connection status', status
        status

    onStart:->
        @setState connected:false, waiting:true, error:null
    onOpenedConn:->
        @setState connected:true, waiting:false
    onClose:->
        @setState connected:false
    onError:(err)->
        console.log 'errror', err
        @setState
            connected:false
            waiting:false
            error:err
    update_path:(e)=>
        console.log 'upd', e.target
        path =  e.target.value
        @setState path:path

    disconnect:()->
        @connector.close()
        @onClose()
    reconnect:()->
        @connector.connect(@state.path)
        @onStart()
    
    render: ->
        status = @getStatus()
        action_text = switch status
            when 'connected' then 'Disconnect'
            when 'disconnected' then 'Connect'
            when 'error' then 'Reconnect'

        L.div className:'widget',
            L.div
                className:'status '+status,
                L.p className:'text'
                    status
            L.div className:'ws-addr',
                L.input type:'text',value:@state.path, onChange:@update_path
            L.div
                className:'act button'
                onClick:@doAction
                action_text



