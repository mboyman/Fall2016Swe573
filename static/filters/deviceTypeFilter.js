'use strict';

app.filter('hasAnyType', [function () {
    return function (device, deviceTypes) {
        if (device) {
            for (var i = 0; i < deviceTypes.length; i++) {
                if (device.Type === deviceTypes[i]) {
                    return true;
                }
            }
        }
        return false;
    };
}]);