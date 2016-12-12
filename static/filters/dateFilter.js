'use strict';

app.filter('parseDate', ["$filter" , function ($filter) {
    return function (input) {
        input = input.replace(/\//g, '');
        var myDate = new Date(input.match(/\d+/)[0] * 1);
        return $filter('date')(myDate, 'dd.MM.yyyy HH:mm:ss');
    };
}]).filter('parseC#Date', [ function () {
    return function (input) {
        input = input.replace(/\//g, '');
        return new Date(input.match(/\d+/)[0] * 1);
    };
}]);