#---------------------------
# File : controllers.coffee
# Author : liki
# Description : Controllers
# Created : 5/17/13
#---------------------------

wioApp.controller 'MainCtrl', ['$scope', ($scope) ->
	$scope.applyStatus = 'pre-register'
	$scope.applyBetaAccount = ->
		$scope.applyStatus = 'email'
]

wioApp.controller 'RegisterCtrl', ['$scope', '$location', '$http', 'AppliedUser', ($scope, $location, $http, AppliedUser) ->
	$scope.validEmail = true
	$scope.register = ->
		$scope.validEmail = $scope.regForm['email'].$dirty and $scope.regForm['email'].$valid and !$scope.regForm['email'].$error.email
		if $scope.validEmail
			$('#registerBtn').attr('disabled', 'disabled')
			email = { email: $scope.email }
			postData = JSON.stringify(email)
			$http.post('/register', postData).success (data) ->
				AppliedUser.set(data)
				$location.path '/applied'
]

wioApp.controller 'AppliedCtrl', ['$scope', 'AppliedUser', ($scope, AppliedUser) ->
	$scope.email = AppliedUser.get()
]

wioApp.controller 'ConfirmCtrl', ['$scope', '$http', ($scope, $http) ->
	$http.get('/static/json/wechat_picks.json').success (data) ->
		$scope.operation = data[0]
		$scope.product = data[1]
]