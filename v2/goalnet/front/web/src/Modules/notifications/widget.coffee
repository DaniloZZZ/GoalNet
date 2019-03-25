
import React, { Component } from 'react'
import L from 'react-dom-factories'
import './notifs.less'
import JsonBeauty from '../../Modules/json_beauty/JsonBeauty.coffee'
L_ = React.createElement

export default class Widget extends React.Component
	constructor:(props)->
		super(props)

	render: ->
		{notifs} = @props
		elems = L.div
			className:'item'
			'No notifications yet'
		if notifs.length>0
			el = []
			for n,i in notifs
				el.push L.div 
						className:'item'
						key:i
						L_ JsonBeauty,0,n
			elems = el
		L.div className:'notif',
			L.div className:'widget',
				elems

