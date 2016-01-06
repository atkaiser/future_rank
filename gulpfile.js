// require gulp
var gulp = require('gulp');

//require other packages
var concat = require('gulp-concat');
var rename = require("gulp-rename");
var jshint = require('gulp-jshint');

// default task
gulp.task('default', function() {
    ['js', 'css', 'watch']
});

//watch task
gulp.task('watch', function() {
    gulp.watch('./static/*.js', ['js']);
    gulp.watch('./static/*.scss', ['css']);
});

// js task
gulp.task('js', function() {
    return gulp.src('./static/*.js')
        .pipe(concat('all.js'))
        .pipe(gulp.dest('./server/static/'));
});

// js hint
gulp.task('jshint', function() {
    return gulp.src('./static/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter("default"));
});

// css task
gulp.task('css', function() {
    return gulp.src('./static/*.css')
        .pipe(concat('all.css'))
        .pipe(gulp.dest('./server/static/'));
});