'use strict';

app.filter('dbmToPercent', [function () {
    return function (num) {
        if (num) {
            var maxStrength = -75, minStrength = -110;
            if (num <= minStrength)
                return 0;
            if (num >= maxStrength)
                return 100;
            return (num - minStrength) *100 / (maxStrength - minStrength);
        }
    };
}]);