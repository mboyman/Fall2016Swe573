'use strict';
app.controller("indexController", ["$scope", "$http", "$location", "$q", "dataFactory", "$translate", function ($scope, $http, $location, $q, dataFactory, $translate) {
    $scope.isLogin = (location.hash === '#/login')
    
  
}]);
