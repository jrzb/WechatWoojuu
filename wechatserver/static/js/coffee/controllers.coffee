#---------------------------
# File : controllers.coffee
# Author : liki
# Description : 
# Created : 4/28/13
#---------------------------

wwAppDep.controller 'MainCtrl', ['$scope', '$location', ($scope, $location) ->
	pathArray = $location.path().split('/')
	# TODO: Find a better way to get userid from url
	$scope.userId = pathArray[2]
]

wwAppDep.controller 'DashboardCtrl', ['$scope', '$http', '$routeParams', '$filter', 'DashboardAPI', 'SharedProperties', ($scope, $http, $routeParams, $filter, DashboardAPI, SharedProperties) ->
	userId = $routeParams.userId

	currWeek = Date.today().getWeek() - 1
	summaryPeriod = SharedProperties.getWeek(currWeek)

	# Summary expense for the year
	summaryParams =
		userid: userId
		categories: ''
		fromdate: summaryPeriod.firstWeekDay
		enddate: summaryPeriod.lastWeekDay
	DashboardAPI.summary(summaryParams, (data) ->
		$scope.summary = data[0]
	)

	# Top category of expenses for the year
	topCategoryParams =
		userid: $routeParams.userId
		fromdate: summaryPeriod.firstWeekDay
		enddate: summaryPeriod.lastWeekDay
		limit: 1
	DashboardAPI.category(topCategoryParams, (data) ->
		$scope.top = data[0]
	)

	# Chart for this week
	chartPeriod = SharedProperties.getWeek(0)
	chartParams =
		userid: userId
		fromdate: chartPeriod.firstWeekDay
		enddate: chartPeriod.lastWeekDay
	DashboardAPI.chart(chartParams, (data) ->
		# Use list comprehension to get the totalamount of everyday expense sum in a week
		weeklyExpenses = (parseInt(daily.totalamount) for daily in data)

		Highcharts.setOptions(
			colors: [
				'rgb(65,105,42)',
				'rgb(29,78,0)',
				'rgb(225,231,217)',
				'rgb(65,105,42)',
				'rgb(29,78,0)',
				'rgb(225,231,217)',
				'rgb(65,105,42)',
				'rgb(29,78,0)',
				'rgb(225,231,217)',
				'rgb(225,231,217)'
			]
		)
		chart =
			chart:
				backgroundColor: null
			credits:
				enabled: false
			subtitle:
				text: null
			legend:
				enabled: false
			exporting:
				enabled: false
			tooltip:
				backgroundColor: 'rgba(225,231,217,0.65)'
				borderWidth: 0
				shadow: false
			xAxis:
				categories: ['周一', '二', '三', '四', '五', '六', '日']
				lineWidth: 0
				tickColor: Highcharts.getOptions().colors[2]
				labels:
					y: 25
					useHTML: true
					style:
						color: Highcharts.getOptions().colors[1]
					formatter: ->
						"Hey #{@value}"
			yAxis:
				showEmpty: false
				gridLineWidth: 1
				gridLineColor: 'rgb(225,231,217)'
				labels:
					style:
						color: Highcharts.getOptions().colors[1]
				title:
					text: null
			plotOptions:
				areaspline:
#					pointStart: firstWeekDay
#					pointInterval: 24 * 3600 * 1000 # one day
					lineWidth: 3
					marker:
						fillColor: 'rgb(225,231,217)'
						lineColor: 'rgb(65,105,42)'
						lineWidth: 4
						radius: 6
			series: [
				name: '今日'
#				data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6]
				data: weeklyExpenses
				fillColor:
					linearGradient : [0, 0, 0, 270]
					stops: [
						[0, 'rgba(29,78,0,0.6)']
						[1, 'rgba(29,78,0,0.05)']
					]
			]

		$scope.weeklyChart = chart
		# Get total for this week
		$scope.weeklyTotal = weeklyExpenses.reduce (x, y) -> x + y
	)

	# Chart period
	# {{ firstWeekDay | dateformat:"M月d日" }} - {{ lastWeekDay | dateformat:"M月d日" }}
#	$scope.firstWeekDay = chartPeriod.firstWeekDay
#	$scope.lastWeekDay = chartPeriod.lastWeekDay

]

wwAppDep.controller 'DetailsCtrl', ['$scope', '$http', '$routeParams', 'DetailsAPI', 'SharedProperties', ($scope, $http, $routeParams, DetailsAPI, SharedProperties) ->
	# List expense helper
	listExpenses = (period) ->
		paramsWeek =
			userid: $routeParams.userId
			fromdate: period.firstWeekDay
			enddate: period.lastWeekDay
		DetailsAPI.list(paramsWeek, (data) ->
			expenseDict = {}
			results = data
			for result in results
				currentDate = Date.parse(result.date).toString("yyyy-MM-dd")
				delete result.date
				if not expenseDict[currentDate]
					expenseDict[currentDate] = [result]
				else
					expenseDict[currentDate].push(result)

			$scope.expenses = (date: k, expenses: v for k, v of expenseDict)

			console.log $scope.expenses
		)

	# Previous x weeks
	prev = 0
	period = SharedProperties.getWeek(prev)

	listExpenses(period)

	$scope.removeExpense = (expenseId, dateIdx, idx) ->
#		console.log "expenseid, dateIdx, idx: #{expenseId}, #{dateIdx}, #{idx}"
		toRemove = window.confirm "确认删除？"
		if toRemove
			paramsExpense =
				userid: $routeParams.userId
				expenseid: expenseId
			DetailsAPI.remove(paramsExpense, (data) ->
				if data.errorcode is "200"
					# Remove current item on ui
					expensesList = $scope.expenses[dateIdx].expenses
					expensesList.splice idx, 1
					# If there no remaining expenses for that date, remove the date as well
					if expensesList.length is 0
						$scope.expenses.splice dateIdx, 1
			)

	$scope.loadPrevWeek = ->
		prev += 1
		period = SharedProperties.getWeek(prev)

		listExpenses(period)
]