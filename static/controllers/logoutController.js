'use strict';
app.controller("logoutController", ["$q", "$scope", "$http", "$location", "dataFactory", function ($q, $scope, $http, $location, dataFactory) {    
    
    dataFactory.accountService.logoutAccount().success(function (data) {
        console.log('logged out');
        // location.href = '/Redirect/Login';
        window.location = data.redirect
    });

}]);
