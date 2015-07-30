var urlParam = function (name) {
  if(name=(new RegExp('[?&]' + encodeURIComponent(name) + '=([^&]*)')).exec(location.search))
    return decodeURIComponent(name[1]);
}

var Preference = React.createClass({
  increase: function() {
    if(this.props.count == 10) {
      return false;
    }
    var new_count = this.props.count + 1;
    this.props.update(this.props.subreddit, new_count, "increase");
  },
  decrease: function() {
    if(this.props.count == 1) {
      return false;
    }
    var new_count = this.props.count - 1;
    this.props.update(this.props.subreddit, new_count, "decrease");
  },
  deleteThis: function() {
    this.props.update(this.props.subreddit, 0, "delete");
  },
  render: function() {
    var decreaseClass = "fa fa-angle-down action-icon possible";
    var increaseClass = "fa fa-angle-up action-icon possible";
    var deleteClass = "fa fa-trash-o action-icon";
    if(this.props.count == 1) {
      decreaseClass = "fa fa-angle-down action-icon impossible";
    } else if(this.props.count == 10) {
      increaseClass = "fa fa-angle-up action-icon impossible";
    }
    return (
      <tr>
        <td>{this.props.subreddit}</td>
        <td>{this.props.count}</td>
        <td>
          <i className={deleteClass} onClick={this.deleteThis}
             data-toggle="tooltip" data-placement="left" title="Delete Subscription"></i>
          <i className={increaseClass} onClick={this.increase}></i>
          <i className={decreaseClass} onClick={this.decrease}></i>
        </td>
      </tr>
    )
  }
});

var PreferencesList = React.createClass({
  updateData: function(subreddit, new_count, action) {
    var data = this.props.data;
    var new_data = data.map(function (pref) {
      if(pref.subreddit == subreddit) {
        if(action=="delete") {return;}
        return {"subreddit": pref.subreddit,
                "count": new_count,
                "id": pref.id}
      } else {
        return pref
      }
    });
    new_data = new_data.filter(function(pref) {return pref != undefined;});
    this.props.saveData(new_data);
  },
  render: function() {
    var updateData = this.updateData;
    var preferenceNodes = this.props.data.map(function (pref) {
      return (
        <Preference subreddit={pref.subreddit} count={pref.count}
                    update={updateData} />
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
  getDataFromServer: function() {
    var member_uuid = urlParam("member");
    var token_uuid = urlParam("token");
    var url = location.origin + location.pathname + "/json/" + location.search;

    $.ajax({
      url: url,
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
  saveDataToServer: function(data) {
    console.log("data to be saved");
    this.setState({data: data});
    console.log(data);
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.getDataFromServer();
  },
  render: function() {
    return (
      <div className="prefrences-box">
        <PreferencesList data={this.state.data} saveData={this.saveDataToServer} />
      </div>
    );
  }
});

React.render(
  <PreferencesBox />,
  document.getElementById('react-container')
);
