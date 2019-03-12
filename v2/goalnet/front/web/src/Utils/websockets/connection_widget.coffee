import React, { Component } from 'react'
import L from 'react-dom-factories'
import style from './connection.less'

L_ = React.createElement

export default class Widget extends React.Component
	state :
		connected:false
		waiting:false
		error:""
		addr:""

	constructor:(props)->
		super(props)
		{connector} = props
		if connector
			connector.setOnStateChange(@onConnectorStateChange)
			@connector = connector
		else
			@state.status='error'
			@state.error='failed to init'

	onConnectorStateChange:(state_id)=>
		switch state_id
			when 'open' then @onOpen()
			when 'error' then @onError()
			when 'closed' then @onClosed()

	getStatus:()->
		{connected,error,waiting} = @state
		console.log 'Current connection status', connected
		status = if connected then 'connected' else 'disconnected'
		console.log 'Current connection status', status
		if waiting
			status = 'waiting'
		if error
			status = 'error'
		console.log 'Current connection status', status
		status

	onStart:->
		@setState connected:false, waiting:true, addr:@connector.api_path
	onOpen:->
		@setState connected:true, waiting:false, error:'', addr:@connector.api_path
	onClose:->
		@setState connected:false, addr:@connector.api_path
	onError:(err)->
		@setState 
			connected:false
			addr:@connector.api_path
			error:err

	doAction:(e)=>
		status = @getStatus()
		switch status
			when 'connected' then @disconnect()
			when 'error' then @reconnect()
			when 'disconnected' then @reconnect()

	disconnect:()->
		@connector.close()
		@onClose()
	reconnect:()->
		@connector.connect()

    
	render: ->
		status = @getStatus()
		action_text = switch status 
			when 'connected' then 'Disconnect'
			when 'disconnected' then 'Reconnect'
			when 'error' then 'Reconnect'

		L.div className:'widget',
			L.div 
				className:'status '+status,
				L.p className:'text'
					status
			L.div
				className:'act button'
				onClick:@doAction
				action_text



