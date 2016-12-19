'use strict';
app.controller("exercisesController", ["$scope", "$http", "$location", "$q", "dataFactory", "notificationFactory", function ($scope, $http, $location, $q, dataFactory, notificationFactory) {

    var apiUrl = '/backend/Api/';
    $scope.userExercises = [];
    $scope.exercises = [];

    var cookie = document.cookie.split('=')
    var username = cookie[0];
    $http.get(apiUrl + 'user/' + username).success(function (result) {
        $scope.user = result;

        $http.get(apiUrl + 'user/' + username + '/exercise').success(function (res) {
            for (var ex in res.list) {
                var ob = res.list[ex];
                ob.exercise.cal = getCalorie(ob.exercise.value, $scope.user.weight)
            }


            $scope.userExercises = res.list
            $http.get(apiUrl + 'exercises').success(function (res) {
                for (var ex in res.list) {
                    var o = res.list[ex]
                    var key = Object.keys(o)[0];
                    $scope.exercises.push({
                        key: key,
                        value: o[key]
                    })
                }
            });
            $scope.add = function () {
                var cookie = document.cookie.split('=')
                var username = cookie[0];
                $http.post(apiUrl + 'user/' + username + '/exercises', $scope.selectedExercise).success(function (res) {
                    $scope.selectedExercise.cal = getCalorie($scope.selectedExercise.value, $scope.user.weight);
                    if ($scope.selectedExercise) {
                        $scope.userExercises.push({
                            'username': username,
                            'exercise': $scope.selectedExercise
                        });
                    }
                });
            };
        });

    });


    function getCalorie(arr, user_weight){
        var cal = 0;
        user_weight = Number(user_weight)
        if(user_weight <= 130)
            cal = arr[0]
        if(user_weight > 130 && user_weight <= 150 )
            cal = arr[1]
        if(user_weight > 150 && user_weight <= 170 )
            cal = arr[2]
        if(user_weight > 170)
            cal = arr[3]
        return cal;
    }




}]);