var urlParam = function (name) {
  if(name=(new RegExp('[?&]' + encodeURIComponent(name) + '=([^&]*)')).exec(location.search))
    return decodeURIComponent(name[1]);
}

var Preference = React.createClass({
  render: function() {
    return (
      <tr>
        <td>{this.props.subreddit}</td>
        <td>{this.props.count}</td>
        <td>
          <i className="fa fa-trash action-icon"></i>
          <i className="fa fa-angle-up action-icon"></i>
          <i className="fa fa-angle-down action-icon"></i>
        </td>
      </tr>
    )
  }
});

var PreferencesList = React.createClass({
  render: function() {
    var preferenceNodes = this.props.data.map(function (pref) {
      return (
        <Preference subreddit={pref.subreddit} count={pref.count}></Preference>
      );
    });
    return (
      <div className="prefernces-list">
        <table className="table">
          <thead>
            <th>Subreddit</th>
            <th>Link Count</th>
            <th>Actions</th>
          </thead>
          <tbody>
            {preferenceNodes}
          </tbody>
        </table>
      </div>
    )
  }
});

var PreferencesBox = React.createClass({
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
      <div className="prefrences-box">
        <PreferencesList data={this.state.data}></PreferencesList>
      </div>
    );
  }
});

React.render(
  <PreferencesBox url="http://localhost:8001/members/preferences/json?member=488ee9af-b9dc-4498-ae29-9260008971c6&token=82fba07b-a840-4fe0-aae8-135651d6546e"/>,
  document.getElementById('react-container')
);
