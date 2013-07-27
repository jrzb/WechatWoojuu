#---------------------------
# File : app.coffee
# Author : liki
# Description : Main App
# Created : 5/17/13
#---------------------------

'use strict'

# wio = wechat.io
wioApp = angular.module 'wioApp', ['ngResource'], ->

wioApp.config ['$routeProvider', '$locationProvider', ($routeProvider, $locationProvider) ->
	$routeProvider.when '/',
		templateUrl: '/static/partials/main.html'
		controller: 'MainCtrl'
	$routeProvider.when '/applied',
		templateUrl: '/static/partials/applied.html'
		controller: 'AppliedCtrl'
	$routeProvider.when '/confirm_email/:emailHash',
		templateUrl: '/static/partials/confirm_email.html'
		controller: 'ConfirmCtrl'
	$routeProvider.otherwise
		redirectTo: '/'

	$locationProvider.html5Mode true
]

# Showing loading spinner on loading $http requests
# http://codingsmackdown.tv/blog/2013/01/02/using-response-interceptors-to-show-and-hide-a-loading-widget/
wioApp.config ['$httpProvider', ($httpProvider) ->
	$http = null
	interceptor = ['$q', '$injector', ($q, $injector) ->
		success = (response) ->
			# get $http via $injector because of circular dependency problem
			$http = $http or $injector.get('$http')
			$('#loadingWidget').hide() if $http.pendingRequests.length < 1
			response
		error = (response) ->
			# get $http via $injector because of circular dependency problem
			$http = $http or $injector.get('$http')
			$('#loadingWidget').hide() if $http.pendingRequests.length < 1
			$q.reject(response)
		(promise) ->
			$('#loadingWidget').show()
			promise.then(success, error)
	]
	$httpProvider.responseInterceptors.push(interceptor)
]