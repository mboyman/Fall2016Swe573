var gulp = require('gulp'),
   notify = require("gulp-notify"),
   print = require("gulp-print"),
   bower = require('gulp-bower'),
   series = require('stream-series'),
   inject = require('gulp-inject'),
   concat = require('gulp-concat'),
   uglify = require("gulp-uglify"),
   ignore = require("gulp-ignore"),
   rimraf = require("rimraf"),
   cssmin = require("gulp-cssmin"),
   merge = require('merge'),
   mainBowerFiles = require('main-bower-files');


//Path definitions
var paths = {
    webroot: ""
};

paths.app = paths.webroot;
paths.appControllers = paths.app + "controllers/";
paths.appFactories = paths.app + "factories/";
paths.appFilters = paths.app + "filters/";
paths.appContent = paths.app + "content/";
paths.libs = paths.webroot + "libraries/";
paths.minified = paths.webroot + "minified/";
paths.minJs = paths.webroot + "minified/js/";
paths.minCss = paths.webroot + "minified/css/";

var jsToConcat = [
    paths.libs + '**/kendo.all.min.js'
];

var appJsLibsArray = [
    paths.app + 'app.js',
    paths.libs + 'custom/*.js',
    paths.appFactories + '**/*.js',
    paths.appFilters + '**/*.js',
    paths.appControllers + '**/*.js'
];
var appCssLibsArray = [
    paths.webroot + '**/*.css',
    '!**/*.min.css',
    '!**/*examples-offline.css',
    '!bower_components/**/*.css',
    '!node_modules/**/*.css'
];
var bowerOptions = {
    "overrides": {
        "pnotify": {
            "main": ["**/pnotify.js", "**/pnotify.confirm.js"]
        },
        "heatmap.js": {
            "main": ["**/src/heatmap.js"]
        }
    }
}

//Inject tasks
gulp.task('inject', function () {
    var vendorJsLibs = gulp.src(mainBowerFiles(merge(bowerOptions, { filter: ['**/*.js'] })), { read: false }).pipe(print());
    var vendorCssLibs = gulp.src(mainBowerFiles({ filter: ['**/*.css'] }), { read: false }).pipe(print());
    var appJsLibs = gulp.src(appJsLibsArray)
    var appCssLibs = gulp.src(appCssLibsArray)
    var jsLibsToConcat = gulp.src(jsToConcat)
    return gulp.src(paths.app + 'index.html')
            .pipe(inject(series(vendorJsLibs, jsLibsToConcat, vendorCssLibs, appJsLibs, appCssLibs), {addRootSlash: false}))
            .pipe(gulp.dest(paths.app))
            .pipe(notify({ message: 'DEV injection is completed' }));
});

gulp.task("inject-min", ['min'], function () {
    var minJsLibs = gulp.src([paths.minJs + "**/vendor.min.js", paths.minJs + "**/app.min.js"], { read: false }).pipe(print());
    var minCssLibs = gulp.src([paths.minCss + "**/*.min.css"], { read: false }).pipe(print());
    return gulp.src(paths.app + 'index.html')
            .pipe(inject(series(minJsLibs, minCssLibs), {addRootSlash: false}))
            .pipe(gulp.dest(paths.app))
            .pipe(notify({ message: 'PROD injection is completed' }));
});

//Minification task
gulp.task("min", function () {
    var minifiedVendorJsLibs = gulp.src(mainBowerFiles(merge(bowerOptions, { filter: ['**/*.js'] }))).pipe(uglify());
    var jsLibsToConcat = gulp.src(jsToConcat);
    //Minify vendor Js files
    series(minifiedVendorJsLibs, jsLibsToConcat)
       .pipe(print())
       .pipe(concat("vendor.min.js"))            
       .pipe(gulp.dest(paths.minJs))
       .pipe(notify({ message: 'Vendor js minification is completed' }));
    //Minify Vendor Css files
    gulp.src(mainBowerFiles({ filter: ['**/*.css'] }))
       .pipe(print())
       .pipe(concat("vendor.min.css"))
       .pipe(cssmin())
       .pipe(gulp.dest(paths.minCss))
       .pipe(notify({ message: 'Vendor css minification is completed' }));
    //Minify App Js files
    gulp.src(appJsLibsArray)
        .pipe(print())
        .pipe(concat("app.min.js"))
        .pipe(uglify())
        .pipe(gulp.dest(paths.minJs))
        .pipe(notify({ message: 'Vendor js minification is completed' }));
    //Minify App Css files
    var kendoImgs = gulp.src([paths.libs + "Kendo/Default/**/*"]).pipe(gulp.dest(paths.minCss + "Default"));
    var telInputImgs = gulp.src(mainBowerFiles({ filter: ['**/intl-tel-input/build/img/**/*'] }) ).pipe(gulp.dest(paths.minified + "img"));
    return gulp.src(appCssLibsArray)
        .pipe(print())
        .pipe(concat("app.min.css"))
        .pipe(cssmin())
        .pipe(gulp.dest(paths.minCss))
        .pipe(notify({ message: 'Vendor css minification is completed' }));
});




gulp.task('main-bower-files', function () {
    return gulp.src(mainBowerFiles(bowerOptions), { read: false }).pipe(print())
});


//Watch
gulp.task('watch:bower', function () {
    gulp.watch(bower.json, ['inject:DEV']);
});

gulp.task('watch:allAppJs', function () {
    gulp.watch([paths.app + '**/*.js'], ['minAppLibs:js']);
});

gulp.task("clean:js", function (cb) {
    rimraf(paths.minified + '**/*.js', cb);
});

gulp.task("clean:css", function (cb) {
    rimraf(paths.minified + '**/*.css', cb);
});
gulp.task("clean", ["clean:js", "clean:css"]);

