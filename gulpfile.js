var gulp = require('gulp');
var source = require("vinyl-source-stream");
var sass = require('gulp-ruby-sass');
var notify = require('gulp-notify');
var react = require('gulp-react');
var rename = require('gulp-rename');
var concat = require('gulp-concat');

gulp.task('sass', function() {
    return sass('./static/sass/', { style: 'expanded' })
        .pipe(gulp.dest('./static/css/'));
});

gulp.task('react', function () {
    return gulp.src('./static/jsx/**/*.jsx')
        .pipe(rename(function(path) {
            path.extname = ".js"
        }))
        .pipe(react())
        .pipe(gulp.dest('./static/js/'));
});

gulp.task('concat', function() {
    return gulp.src(['./static/js/preferences.js', './static/js/main.js'])
        .pipe(concat('all.js'))
        .pipe(gulp.dest('./static/js/'));
});

gulp.task('watch', function () {
    var watcher_sass = gulp.watch('./static/sass/**/*.scss', ['sass']);
    watcher_sass.on('change', function(event) {
        console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
    });

    var watcher_react = gulp.watch('./static/jsx/*.jsx', ['react']);
    watcher_react.on('change', function(event) {
        console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
    });

    var watcher_concat = gulp.watch(['./static/js/**/*.js'], ['concat']);
    watcher_concat.on('change', function(event) {
        console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
    })
});
