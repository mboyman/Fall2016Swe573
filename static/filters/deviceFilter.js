'use strict';

app.filter('hasAnyDevice', [function () {
    return function (device, devices) {
        if (device) {
            for (var i = 0; i < devices.length; i++) {
                if (device.DeviceHWID == devices[i].DeviceHWID) {
                    return true;
                }
            }
        }
        return false;
    };
}]);