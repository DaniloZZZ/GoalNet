
import React, { Component } from 'react'
import L from 'react-dom-factories'
import { Form, Field } from 'react-final-form'
import ConnectionWidget from '../../Utils/websockets/connection_widget.coffee'
import NotificationWidget from '../../Modules/notifications/widget.coffee'
import JsonBeauty from '../../Modules/json_beauty/JsonBeauty.coffee'
import {Connector} from '../../Utils/websockets/connector.coffee'
L_ = React.createElement

get_api_path = ->
	"""
	Gets the api for websockets server
	"""
	host = window.location.hostname
	port =10002
	api_path = 'ws://'+ host+':'+port
	api_path

export default class Page extends React.Component
	state:
		notifs:[]
	constructor:(props)->
		super(props)
		api_path = get_api_path()
		@connector = new Connector(api_path:api_path)
		@connector.onMessage = @onNotif

	onNotif:(notif)=>
		@setState (s,p)->
			s.notifs.unshift JSON.parse(notif.data)
			s

	send:(form)=>
		console.log 'Sending', form
		@connector.send(JSON.stringify(form))

	render: ->
		capitalize = (s) -> s[0].toUpperCase() + s.slice(1)
		field = (key)->
			L.div 0,
				L.label 0,capitalize(key)
				L_ Field, name:key,component:'input'
		L.div 0,
			L.h2 0, "Admin panel for GoalNet"
			L_ ConnectionWidget, connector:@connector
			L_ NotificationWidget, notifs:@state.notifs
			L_ Form,
				onSubmit:@send
				render:({handleSubmit})->
					L.form onSubmit:handleSubmit,
						L.h2 0, "Compose a message"
							field 'type'
							field 'app'
						L.button type:'submit', 'Send'
							

