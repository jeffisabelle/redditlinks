var PreferencesBox = React.createClass({displayName: "PreferencesBox",
  render: function() {
    return (
      React.createElement("div", {className: "prefrences-box"}, 
        "Hello, there"
      )
    );
  }
});

React.render(
  React.createElement(PreferencesBox, null),
  document.getElementById('react-container')
);
