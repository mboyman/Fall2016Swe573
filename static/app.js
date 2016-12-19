var app = angular.module("DietApp", ['ngRoute', 'angularUtils.directives.dirPagination', 'angular-loading-bar', 'kendo.directives', 'ngFileSaver', 'pascalprecht.translate', 'ngSanitize', 'ngIntlTelInput']);

app.config(["$routeProvider", "$httpProvider", "$translateProvider", "$locationProvider", "ngIntlTelInputProvider", function ($routeProvider, $httpProvider, $translateProvider, $locationProvider, ngIntlTelInputProvider) {
    //$httpProvider.defaults.useXDomain = true;

    //Home
    $routeProvider.when("/home", {
        controller: "homeController",
        templateUrl: "views/home.html"
    });

    //User
    $routeProvider.when("/food", {
        controller: "foodController",
        templateUrl: "views/food.html"
    });

    $routeProvider.when("/fooddetails/:id", {
        controller: "foodDetailsController",
        templateUrl: "views/foodDetails.html"
    });

    $routeProvider.when("/myfood", {
        controller: "myfoodController",
        templateUrl: "views/myfood.html"
    });

    $routeProvider.when("/exercises", {
        controller: "exercisesController",
        templateUrl: "views/exercises.html"
    });


    // login
    $routeProvider.when("/login", {
        controller: "loginController",
        templateUrl: "views/login.html"
    });

    //logout
    $routeProvider.when("/auth/logout/", {
        controller: "logoutController",
        templateUrl: "views/account.html"
    });

    $routeProvider.otherwise({
        redirectTo: "/home"
    });

    $httpProvider.interceptors.push('appInterceptor');



}]).run(["$rootScope", "$location", "$q", function ($rootScope, $location, $q) {
    //console.log('$rootScope Geldi');

    $rootScope.$on('$viewContentLoaded', function () {
        //console.log('Geldi');

    });
}]);