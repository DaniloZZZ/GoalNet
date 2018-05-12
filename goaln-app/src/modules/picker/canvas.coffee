React = require 'react'

ReactDOM = require 'react-dom'
moment = require 'moment'

import DOM from 'react-dom-factories'
import config from '../../config.js'
import { Form, Text, TextArea, Checkbox } from 'react-form'

axios =  require 'axios'
# Assign React to Window so the Chrome React Dev Tools will work.

{Component}= React
L = DOM
C = React.CreateClass
l = console.log

detectPos = (e)=>
	[x,y]=[0,0]
	e = if e then e else window.event
	x = e.pageX || x
	y = e.pageY || y
	if e.clientX
		x = e.clientX
		+ document.body.scrollLeft
		+ document.documentElement.scrollLeft
	if e.clientY
		y = e.clientY
		+ document.body.scrollTop
		+ document.documentElement.scrollTop
	return [x,y]

class Canvas extends Component
	constructor: (props)->
		l props
		super()
		@state =
			dates:[]

	mMove:(e)=>
		l 'enter'
		[x,y] = detectPos(e)
		self= ReactDOM.findDOMNode(@refs['canvas-pos'])
			.getBoundingClientRect()
		[x,y] = [x - self.x, y - self.y]
		@setState
			x:x
			y:y
	mUp:=>
		l 'Up'
	mDown:=>
		l 'Down'

	render: ->
		L.div
			className:'canvas'
			ref:'canvas-pos'
			style:
				backgroundColor:'red'
				width:'100%'
				height:'calc(100% - 10px)'

			onMouseMove:	@mMove
			onMouseUp:		@mUp
			onMouseDown:	@mDown
			@state.x
			' '
			@state.y

export default Canvas
	
