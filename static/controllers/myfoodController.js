'use strict';
app.controller("myfoodController", ["$scope", "$http", "$location", "$q", "dataFactory", "notificationFactory", function ($scope, $http, $location, $q, dataFactory, notificationFactory) {

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

    $scope.add = function (food) {
        var cookie = document.cookie.split('=')
        var username = cookie[0];
        $http.post(apiUrl + 'user/'+ username +'/food', food).success(function (res) {
            if(food){
                $scope.userFoods.push({'username': username, 'food': food});
            }
        });
    };

    $scope.search = function () {
        if(!$scope.searchTerm){
            return;
        }
        $http.get(apiUrl + 'food?q='+ $scope.searchTerm).success(function (res) {
            $scope.foodList = res.list.list;
            
        });
    };

}]);