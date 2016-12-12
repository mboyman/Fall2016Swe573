'use strict';
app.controller("foodController", ["$scope", "$http", "$location", "$q", "dataFactory", "notificationFactory", function ($scope, $http, $location, $q, dataFactory, notificationFactory) {

    var apiUrl = '/backend/Api/';
    $scope.userFoods = [];
    $http.get(apiUrl + 'food').success(function (res) {
        $scope.food = res.list
    });
    var cookie = document.cookie.split('=')
    var username = cookie[0];
    $http.get(apiUrl + 'user/'+ username+ '/food').success(function (res) {
        $scope.userFoods = res.list
        
    });

    $scope.add = function () {
        var cookie = document.cookie.split('=')
        var username = cookie[0];
        $http.post(apiUrl + 'user/'+ username +'/food', $scope.selectedFood).success(function (res) {
            if($scope.selectedFood){
                $scope.userFoods.push({'username': username, 'food': $scope.selectedFood});
            }
        });
    };


}]);