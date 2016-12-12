'use strict';
app.factory('appInterceptor', ["$q", "$location", function dataFactory($q, $location) {
    return {
        // optional method
        'request': function (config) {

            return config;
        },

        // optional method
        'requestError': function (rejection) {

            return $q.reject(rejection);
        },

        // optional method
        'response': function (response) {

            return response;
        },

        // optional method
        'responseError': function (rejection) {

            if (rejection.status == 403)
            {
                location.href = ""
            }

            if (rejection.data.hasOwnProperty('LoginLink')) {
                location.href = rejection.data.LoginLink;
            }
            return $q.reject(rejection);
        }
    };
}]);