#---------------------------
# File : directive.coffee
# Author : liki
# Description : Directives
# Created : 5/17/13
#---------------------------

# ui-if, a successor to ng-show/hide that is almost always needed
# http://angular-ui.github.io/ui-utils/
wioApp.directive 'uiIf', ->
	transclude: 'element'
	priority: 1000
	terminal: true
	restrict: 'A'
	compile: (elem, attrs, transclude) ->
		(scope, elem, attrs) ->
			scope.$watch attrs['uiIf'], (newValue) ->
				childElement = null
				childScope = null
				if childElement
					childElement.remove()
					childElement = undefined
				if childScope
					childScope.$destroy()
					childScope = undefined
				if newValue
					childScope = scope.$new()
					transclude childScope, (clone) ->
						childElement = clone
						elem.after(clone)