import React, { Component } from 'react'
import L from 'react-dom-factories'
import { BrowserRouter as Router, Switch, Route, Redirect, Link } from "react-router-dom"
import 'babel-polyfill'
import 'react-big-calendar/lib/less/styles.less'
import LoginPage from './Pages/login/login.coffee'
import LandingPage from './Pages/landing/main.coffee'
import HomePage from './Pages/home/home.coffee'
import VkAuthPage from './Pages/vk/auth.coffee'
import StatsPage from './Pages/statistics/stats.coffee'
import CalendarPage from './Pages/calendar/calendar.coffee'
import SettingsPage from './Pages/settings/settings.coffee'
import ProjectsPage from './Pages/projects/projects.coffee'
import AdminPage from './admin/config/page.coffee'
import {logged_in,debug_login} from './Utils/sessions.coffee'
import Menu from './Modules/menu/menu.coffee'
L_ = React.createElement

##


export default class App extends React.Component
  state:{}
  constructor:->
    super()
    @state.logged_in = false
    @state.auth_checked = false
    @check_login()

  check_login: ->
    logged_in().then (uid)=>
      console.log 'uid',uid
      if not uid
        console.log "not logged in!"
        @setState auth_checked:true, uid:false
      else:
        @setState auth_checked:true, uid:uid
      if uid=='1'
        console.log "Logged in as dev"
        
  welcomeOrComponent:(component)->
    if not @state.auth_checked
      L_ WaitAuth, 0,0
    else
      if not @state.uid
          console.log('notlogged')
          L_ Redirect, to:'/',0
        else
          console.log('logged')
          component
     
  render: ->
    console.log('App render. app:',this)
    appComponent = ()=>
      console.log 'rendering app'
      L.div 0,
        L_ Menu
        L.div className:'main',
          L_ Route,
            exact: true
            path:'/'
            render: =>
              console.log 'route /'
              L_ HomePage, uid:@state.uid
          L_ Route,
            path:'/vkauth'
            render: =>
              @welcomeOrComponent L_ VkAuthPage, uid:@state.uid,0
          L_ Route,
            path:'/statistics'
            render: =>
              @welcomeOrComponent L_ StatsPage,uid:@state.uid,0
          L_ Route,
            path:'/calendar'
            render: =>
              @welcomeOrComponent L_ CalendarPage, uid:@state.uid,0
          L_ Route,
            path:'/settings'
            render: =>
              @welcomeOrComponent L_ SettingsPage, uid:@state.uid,0
          L_ Route,
            path:'/projects'
            render: =>
              @welcomeOrComponent L_ ProjectsPage, uid:@state.uid,0
          L_ Route,
            path:'/ADMIN'
            render: =>
              @welcomeOrComponent L_ AdminPage, uid:@state.uid,0

    L_ Router, null,
      L.div 0,
        L_ Switch,0,
          L_ Route,
            path:'/login'
            component:LoginPage
          L_ Route,
            path:'/'
            render: ()=>
              if @state.uid
                return appComponent()
              else
                L_ LandingPage

WaitAuth= ()->
  L.div 0,
    L.h2 0, "Authentication..."


