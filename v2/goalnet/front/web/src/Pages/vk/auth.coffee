
import React, { Component } from 'react'
import L from 'react-dom-factories'
import axios from 'axios'

import {Link } from "react-router-dom"

VK_SERVER = 'http://localhost:8990/'
status = 1024
friends = 2
notify = 1
mask = status+friends+notify
VK_AUTH_LINK = 'https://oauth.vk.com/authorize'+'?client_id=6873513&display=page&redirect_uri=http://localhost:8080/vkauth&scope='+mask+'&response_type=token&v=5.92&state=123456'
L_ = React.createElement

export default class Page extends Component
  state:
    auth_status:"NONE"
  constructor: ({uid})->
    super()
    @uid = uid

    ##
    url_string = window.location.href
    console.log 'url', url_string

    token = url_string.match(/token=(.*?)(&|$)/)?[1]
    vkid = url_string.match(/user_id=(.*?)(&|$)/)?[1]
    if not token
      return
    console.log 'token', token
    console.log 'vkid', vkid
    console.log 'uid', @uid
    ##
    @token = token
    @vkid = vkid
    @save_new_token(@uid, vkid, token)

  save_new_token:(uid, vkid, token)->
    axios.get VK_SERVER+'new_auth',
      params:
        access_token:token
        user_id:uid
        vk_user_id:vkid
    .then (r)=>
      console.log("newuser",r)
      if r.data.split(':')[0]=='FAIL'
        @setState auth_status:'FAIL'
      else
        @setState auth_status:'OK'

  render: ->
    L.div null,
      L.h1 null, 'Auth'
      if @state.auth_status=="OK"
        L.h3 null, 'You\'re logged with token:'+@token
      else
        L.a href:VK_AUTH_LINK,'Authorise vk'
      if @state.auth_status=="FAIL"
        L.h3 null, 'Fail'

