var substringMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substringRegex;

    // an array that will be populated with substring matches
    matches = [];

    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      if (substrRegex.test(str)) {
        matches.push(str);
      }
    });

    cb(matches);
  };
};


$(document).ready(function() {
    $.get("/subs/subreddits/json/", function(response) {
        console.log(response);
        $('.typeahead').typeahead({
            minLength: 3,
            highlight: true
        }, {
            name: 'my-dataset',
            source: substringMatcher(response["subreddits"])
        })
    });

    $.get("/members/timezones/json/", function(response) {
        console.log(response);
        $('.typeahead-timezone').typeahead({
            minLength: 3,
            highlight: true
        }, {
            name: 'my-dataset2',
            source: substringMatcher(response["timezones"])
        })
    });
});

$(document).ready(function() {
    var tz = jstz.determine();
    var tz_name = tz.name();

    $("#timezone").val(tz_name);
});
