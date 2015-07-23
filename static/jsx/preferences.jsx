var PreferencesBox = React.createClass({
  render: function() {
    return (
      <div className="prefrences-box">
        Hello, there
      </div>
    );
  }
});

React.render(
  <PreferencesBox />,
  document.getElementById('react-container')
);
