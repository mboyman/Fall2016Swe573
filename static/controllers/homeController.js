'use strict';
app.controller("homeController", ["$scope", "$http", "$location", "$q", "dataFactory", "$translate", "FileSaver", function ($scope, $http, $location, $q, dataFactory, $translate, FileSaver) {
    $scope.isLogin = (location.hash === '#/login')
    

}]);
