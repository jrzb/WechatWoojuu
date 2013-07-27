#---------------------------
# File : directive.coffee
# Author : liki
# Description : 
# Created : 5/15/13
#---------------------------

# https://github.com/rootux/angular-highcharts-directive/blob/master/src/directives/highchart.js
wwAppDep.directive 'chart', ->
	restrict: 'E'
	template: '<div></div>'
	transclude: true
	replace: true

	link: (scope, elem, attrs) ->
		chartsDefaults =
			chart:
				renderTo: elem[0]
				type: attrs.type or null
				height: attrs.height or null
				width: attrs.width or null
			title:
				text: attrs.title or null
		# Update when charts data changes
		scope.$watch( ->
			attrs.value
		, (value) ->
			return true if not attrs.value
			# We need deep copy in order to NOT override original chart object.
            # This allows us to override chart data member and still the keep
            # our original renderTo will be the same
			deepCopy = true
			newSettings = {}
			$.extend(deepCopy, newSettings, chartsDefaults, JSON.parse(attrs.value))
			chart = new Highcharts.Chart(newSettings)
		)
