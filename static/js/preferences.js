var urlParam = function (name) {
  if(name=(new RegExp('[?&]' + encodeURIComponent(name) + '=([^&]*)')).exec(location.search))
    return decodeURIComponent(name[1]);
}

var Preference = React.createClass({displayName: "Preference",
  render: function() {
    return (
      React.createElement("tr", null, 
        React.createElement("td", null, this.props.subreddit), 
        React.createElement("td", null, this.props.count), 
        React.createElement("td", null, 
          React.createElement("i", {className: "fa fa-trash action-icon"}), 
          React.createElement("i", {className: "fa fa-angle-up action-icon"}), 
          React.createElement("i", {className: "fa fa-angle-down action-icon"})
        )
      )
    )
  }
});

var PreferencesList = React.createClass({displayName: "PreferencesList",
  render: function() {
    var preferenceNodes = this.props.data.map(function (pref) {
      return (
        React.createElement(Preference, {subreddit: pref.subreddit, count: pref.count})
      );
    });
    return (
      React.createElement("div", {className: "prefernces-list"}, 
        React.createElement("table", {className: "table"}, 
          React.createElement("thead", null, 
            React.createElement("th", null, "Subreddit"), 
            React.createElement("th", null, "Link Count"), 
            React.createElement("th", null, "Actions")
          ), 
          React.createElement("tbody", null, 
            preferenceNodes
          )
        )
      )
    )
  }
});

var PreferencesBox = React.createClass({displayName: "PreferencesBox",
  loadCommentsFromServer: function() {
    var member_uuid = urlParam("member");
    var token_uuid = urlParam("token");
    console.log(member_uuid);
    console.log(token_uuid);

    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(response) {
        this.setState({data: response["data"]});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.loadCommentsFromServer();
  },
  render: function() {
    return (
      React.createElement("div", {className: "prefrences-box"}, 
        React.createElement(PreferencesList, {data: this.state.data})
      )
    );
  }
});

React.render(
  React.createElement(PreferencesBox, {url: "http://localhost:8001/members/preferences/json?member=488ee9af-b9dc-4498-ae29-9260008971c6&token=82fba07b-a840-4fe0-aae8-135651d6546e"}),
  document.getElementById('react-container')
);
