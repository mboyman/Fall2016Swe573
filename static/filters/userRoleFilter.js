'use strict';

app.filter('hasAnyRole', [function () {
    return function (user, roleNames) {
        if (user) {
            for (var i = 0; i < roleNames.length; i++) {
                for (var j = 0; j < user.Roles.length; j++) {
                    if (user.Roles[j] === roleNames[i]) {
                        return true;
                    }
                }
            }
        }
        return false;
    };
}]);