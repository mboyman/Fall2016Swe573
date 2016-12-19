'use strict';
app.controller("foodDetailsController", ["$scope", "$http", "$location", "$q", "dataFactory", "notificationFactory", function ($scope, $http, $location, $q, dataFactory, notificationFactory) {

    var apiUrl = '/backend/Api/';
    var ind = $location.url().lastIndexOf('/')+1;
    var foodNo = $location.url().substr(ind)
    $scope.userFoods = [];

    $http.get(apiUrl + 'food/'+ foodNo+'/nutrient').success(function (res) {
        $scope.foodNutrient = res.report;
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

    

}]);