#---------------------------
# File : services.coffee
# Author : liki
# Description : Services
# Created : 5/17/13
#---------------------------
#wwAppDep.factory 'DetailsAPI', ['$resource', ($resource) ->
#	$resource(
#		'http://h.woojuu.cc/:api'
#		{api: 'list_expense'}
#		list:
#			method: 'GET'
#			params:
#				userid: '@userid'
#				fromdate: '@fromdate'
#				enddate: '@enddate'
#			isArray: true
#		remove:
#			method: 'POST'
#			params:
#				api: 'delete_expense'
#				userid: '@userid'
#				expenseid: '@expenseid'
#	)
#]

wioApp.service 'AppliedUser', ->
	appliedUser = {}
	return {
		set: (data) -> appliedUser = data
		get: -> appliedUser
	}