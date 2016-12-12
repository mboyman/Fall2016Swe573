var app = angular.module("SynapseApp", ['ngRoute', 'angularUtils.directives.dirPagination', 'angular-loading-bar', 'kendo.directives', 'ngFileSaver', 'pascalprecht.translate', 'ngSanitize', 'ngIntlTelInput']);

app.config(["$routeProvider", "$httpProvider", "$translateProvider", "$locationProvider", "ngIntlTelInputProvider", function ($routeProvider, $httpProvider, $translateProvider, $locationProvider, ngIntlTelInputProvider) {
    //$httpProvider.defaults.useXDomain = true;

    //Home
    $routeProvider.when("/home", {
        controller: "homeController",
        templateUrl: "Views/home.html"
    });

    //User
    $routeProvider.when("/food", {
        controller: "foodController",
        templateUrl: "Views/food.html"
    });

    $routeProvider.when("/exercises", {
        controller: "exercisesController",
        templateUrl: "Views/exercises.html"
    });

    // login
    $routeProvider.when("/login", {
        controller: "loginController",
        templateUrl: "Views/login.html"
    });

    //logout
    $routeProvider.when("/auth/logout/", {
        controller: "logoutController",
        templateUrl: "Views/account.html"
    });

    $routeProvider.otherwise({ redirectTo: "/home" });

    $httpProvider.interceptors.push('appInterceptor');

   

}]).run(["$rootScope", "$location", "$q", function ($rootScope, $location, $q) {
    //console.log('$rootScope Geldi');

    $rootScope.$on('$viewContentLoaded', function () {
        //console.log('Geldi');

    });
}]);
