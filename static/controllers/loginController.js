'use strict';
app.controller("loginController", ["$scope", "$q", "$http", "dataFactory", "$location", function ($scope, $q, $http, dataFactory, $location) {
    var apiUrl = '/backend/Api/';

    $scope.operation = 'login';
    $scope.genders = ['Male', 'Female'];


    $scope.login = function (user) {
        $scope.notify = '';
        var postData = {
            username: $scope.username,
            password: $scope.password
        }
        $http.post(apiUrl + 'user/login', postData).success(function (res) {
            if (res.message === 'user not found') {
                $scope.notify = 'Check user name and password';
            } else {
                $scope.notify = '';
            }
            if (res.message === 'logged in') {
                //new PNotify({ title: 'User logged in',  type: 'success' });
                window.location = '#/home';
            }
        });
    };
    $scope.signup = function (user) {
        $scope.notify = '';
        if ($scope.password !== $scope.password2) {
            $scope.notify = 'Passwords are not equal';
            return;
        }
        var postData = {
            username: $scope.username,
            password: $scope.password,
            name: $scope.name,
            surname: $scope.surname,
            gender: $scope.gender,
            height: $scope.height,
            weight: $scope.weight
        }
        $http.post(apiUrl + 'user/signup', postData).success(function (res) {
            if (res.message === 'user exists') {
                $scope.notify = 'This user name already exists';
            } else {
                $scope.notify = '';
            }
            if (res.message === 'user added') {
                $scope.notify = 'Successfuly signed up';
                window.location = '#/home';
                //new PNotify({ title: 'User added',  type: 'success' });
            }
        });
    };
    $scope.changeOperation = function () {
        if ($scope.operation === 'login') {
            $scope.operation = 'signup';
        } else {
            $scope.operation = 'login';
        }

    };

}]);