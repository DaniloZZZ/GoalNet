React = require 'react'

ReactDOM = require 'react-dom'
moment = require 'moment'

import DOM from 'react-dom-factories'
config =  require process.env.GOALNET_CONFIG_FILE
import { Form, Text, TextArea, Checkbox } from 'react-form'
import './picker.css'
import 'moment'

axios =  require 'axios'
# Assign React to Window so the Chrome React Dev Tools will work.
{Component}= React
L = DOM
C = React.CreateElement
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
		super(props)
		ref = React.createRef()
		@state =
			dates:[]
			vr:2
			item:null
			step:3
			ref:ref

	componentDidMount:()=>
		height = @state.ref.current.clientHeight
		@setState
			height:height
			step:height/60/24*15
	@getDerivedStateFromProps:(props,state)=>
		if not props.children
			return
		h=Canvas.getHeight(state)
		children = props.children.map (i)->
			copy=Object.assign {},i
			copy.start=Canvas.moment2pix(i.start,h)
			copy.end=Canvas.moment2pix(i.end,h)
			return copy
		Object.assign state, children:children

	@getHeight:(state)->
		if not state.height
			h = 0
		else
			h = (state.ref.current||{}).clientHeight||0
	@pix2moment:(pix,h,day)=>
		# day is moment() objerct
		min = 60*24/h*pix
		# to int
		hour = (min /60)|0
		min = min%60|0
		# normally day is moment object but need to copy it
		ret = moment(day)||moment()
		ret = ret.set hour:hour, minute:min
	@moment2pix:(mom,h)=>
		# convert to moment if received a str
		mom=moment(mom)
		mins=60*mom.hour()+mom.minute()
		pix=h*mins/24/60

	getRelPos:(e)->
		[x,y] = detectPos(e)
		self= @state.ref.current
			.getBoundingClientRect()
		[x - self.x, y - self.y]

	mMove:(touch=false)->(e)=>
		e= if touch then e.changedTouches[0] else e
		[x,y]=@getRelPos(e)
		if @state.item
			item=Object.assign @state.item,
				end:y-y%@state.step
		else
			item = null
		@setState
			x:x
			y:y
			item:item

	mUp:(touch=false)-> (e)=>
		e= if touch then e.changedTouches[0] else e
		if @state.item || touch
			if @state.item
				@itemCreated (@state.item)
			@setState item:null
		else
			[x,y] = @getRelPos(e)
			@mousePressed=true
			@setState
				item:
					start:y-y%@state.step
					end:y-y%@state.step

	mDown:(touch=false)-> (e)=>
		if touch
			e = e.changedTouches[0]
			[x,y] = @getRelPos(e)
			@mousePressed=true
			@setState
				item:
					start:y-y%@state.step
					end:y-y%@state.step

	itemCreated:(item_orig)->
		item = JSON.parse JSON.stringify item_orig
		l 'created', item
		item.start=Canvas.pix2moment item.start,
			Canvas.getHeight @state
			@props.date
		item.end=Canvas.pix2moment item.end,
			Canvas.getHeight @state
			@props.date
		l 'created', item
		@props.onItemCreate(item)

	pix2hour:(pix)->
		mom=Canvas.pix2moment pix,
			Canvas.getHeight @state,
			@props.date
		mom.format('HH:mm')

	elem: (i)=>
			foo= L.div
				style:
					backgroundColor:'#bcc'
					top:Math.min(i.start,i.end)
					height:Math.abs(i.end-i.start),
					width:'96%'
					left:'2%'
					position:'absolute'
				key:i.id
				L.div
					className:'goal-time'
					i.goal_title||'goal ', i.id
				L.div
				L.div
					className:'picker-date'
					style: top:'-14px'
					@pix2hour(i.start)
				L.div
					className:'picker-date'
					style: bottom:'0px'
					@pix2hour(i.end)

	render: ->
		i = @state.item
		foo = ''
		if @state.item
			foo=@elem(i)
		ch =@state.children
		if ch
			elems = ( @elem(i) for i in ch)
		L.div
			className:'canvas'
			ref:@state.ref
			style:
				backgroundColor:'#efe'
				#height:'calc(100% - 10px)'
				margin:'3px'
				width: if @state.hover then '110px' else'60px'
				#height:'300px'
				borderRadius:'0.3em'
				position:'relative'
				fontSize:'15px'
				float:'left'

			onMouseMove:	@mMove()
			onMouseUp:		@mUp()
			onMouseDown:	@mDown()
			onMouseLeave:	()=>@setState item:null,hover:false
			onTouchStart:	@mDown true
			onTouchMove:	@mMove true
			onTouchEnd:		@mUp true
			onMouseEnter:	(e)=>@setState hover:true
			foo
			elems
			L.div
				style: margin:'3px'
				@props.date.format('dddd')
			L.div
				className:'canvas'
				style:
					backgroundColor:'black'
					height:'3px'
					width:'100%'
					position:'absolute'
					top:@state.y
					display: if @state.hover then '' else'none'
				L.div
					style:
						fontSize:'14px'
						display: if @state.hover then '' else'none'
					@pix2hour(@state.y)

export default Canvas
	
