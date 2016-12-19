'use strict';
app.controller("indexController", ["$scope", "$http", "$location", "$q", "dataFactory", "$translate", function ($scope, $http, $location, $q, dataFactory, $translate) {
    $scope.isLogin = (location.hash === '#/login')
    var apiUrl = '/backend/Api/';

    $scope.logout = function () {
        var cookie = document.cookie.split('=')
        var username = cookie[0];
        $http.post(apiUrl + 'user/logout', {
            username: username
        }).success(function (res) {
            if (res && res.redirect) {
                location.href = res.redirect;
            } else if (res && res.reload) {
                location.reload(true);
            }
        });
    }

}]);