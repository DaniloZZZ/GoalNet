
import React, { Component } from 'react'
import L from 'react-dom-factories'
import './json_styles.less'
L_ = React.createElement

obj2dom = (obj)->
	switch typeof obj
		#when 'list'   then obj.map obj2dom
		when 'string' then L.div className:'json text', obj
		when 'number' then L.div className:'json text number', obj
		when 'object' then for key, value of obj
			L.div className:'json objet',
				L.div className:'json label',
					key
				obj2dom value

export default class Module extends React.Component
	constructor:(props)->
		super(props)

	render: ->
		obj2dom @props.children

