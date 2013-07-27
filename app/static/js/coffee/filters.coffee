#---------------------------
# File : filters.coffee
# Author : liki
# Description : 
# Created : 5/3/13
#---------------------------

# Override angularjs native currency filter by integrate it with accounting.js
# http://josscrowcroft.github.io/accounting.js/
# sample: {{ value | currency:"$":2:",":".":"%s%f" }}
wwAppDep.filter 'currency', ->
	(num, symbol="$", precision=2, thousand=",", decimal=".", format="%s%f") ->
		accounting.formatMoney num, symbol, precision, thousand, decimal, format

# Customize date format output by using Date.js
# Date format reference: http://code.google.com/p/datejs/wiki/FormatSpecifiers
wwAppDep.filter 'dateformat', ->
	(date, format="yyyy-MM-dd") ->
		Date.parse(date).toString(format)

# No empty string is allowed for notes in details
wwAppDep.filter 'isnotes', ->
	(str) ->
		if str is ""
			notes = "未知消费" if str is ""
		else
			notes = str