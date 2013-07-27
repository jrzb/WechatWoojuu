#---------------------------
# File : controllers.coffee
# Author : liki
# Description :
# Created : 5/1/13
#---------------------------

wwAppDep.service 'SharedProperties', ['$filter', ($filter) ->
	@getWeek = (weeks) ->
		# Get first and last date of current week
		weeks ?= 0
		days = -(weeks * 7)
		if Date.today().is().sunday()
			firstDay = Date.previous().monday().addDays(days)
		else
			firstDay = Date.monday().addDays(days)
		lastDay = Date.next().monday().addSeconds(-1)

		obj =
			firstWeekDay: $filter('date') firstDay, 'yyyy-MM-dd HH:mm:ss'
			lastWeekDay: $filter('date') lastDay, 'yyyy-MM-dd HH:mm:ss'

		return obj
]

wwAppDep.factory 'DashboardAPI', ['$resource', ($resource) ->
	$resource(
		'http://h.woojuu.cc/:api'
		{api: 'summary'}
		summary:
			method: 'GET'
			params:
				userid: '@userid'
				categories: '@categories'
				fromdate: '@fromdate'
				enddate: '@enddate'
			isArray: true
		category:
			method: 'GET'
			params:
				api: 'topn_category'
				userid: '@userid'
				fromdate: '@fromdate'
				enddate: '@enddate'
				limit: '@limit'
			isArray: true
		chart:
			method: 'GET'
			params:
				api: 'summary_daily'
				userid: '@userid'
				fromdate: '@fromdate'
				enddate: '@enddate'
			isArray: true
	)
]

wwAppDep.factory 'DetailsAPI', ['$resource', ($resource) ->
	$resource(
		'http://h.woojuu.cc/:api'
		{api: 'list_expense'}
		list:
			method: 'GET'
			params:
				userid: '@userid'
				fromdate: '@fromdate'
				enddate: '@enddate'
			isArray: true
		remove:
			method: 'POST'
			params:
				api: 'delete_expense'
				userid: '@userid'
				expenseid: '@expenseid'
	)
]
