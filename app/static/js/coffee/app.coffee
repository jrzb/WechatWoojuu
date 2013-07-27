# -*- coding: utf-8 -*-
##---------------------------
## @copyright 2013
## File : app.coffee
## Author : liki
## Description :
## --
## Created : 2013/4/28
##--------------------------- 
'use strict'

# ww = Woojuu for WeChat
wwApp = angular.module 'wwApp', ['wwAppDep']
wwAppDep = angular.module 'wwAppDep', ['ngResource']

wwAppDep.config ['$routeProvider', '$locationProvider', ($routeProvider, $locationProvider) ->
	$routeProvider.when '/',
		templateUrl: '/static/partials/no.html'
	$routeProvider.when '/u/:userId',
		templateUrl: '/static/partials/dashboard.html'
		controller: 'DashboardCtrl'
	$routeProvider.when '/u/:userId/details',
		templateUrl: '/static/partials/details.html'
		controller: 'DetailsCtrl'
	$routeProvider.otherwise
		redirectTo: '/'

	$locationProvider.html5Mode true
]