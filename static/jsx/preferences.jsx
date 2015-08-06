var urlParam = function (name) {
  if(name=(new RegExp('[?&]' + encodeURIComponent(name) + '=([^&]*)')).exec(location.search))
    return decodeURIComponent(name[1]);
}

if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.slice(0, str.length) == str;
  };
}

var Preference = React.createClass({
  increase: function() {
    if(this.props.count == 10) {
      return;
    }
    var new_count = this.props.count + 1;
    this.props.update(this.props.subreddit, new_count, "increase");
  },
  decrease: function() {
    if(this.props.count == 1) {
      return;
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
             data-toggle="tooltip" data-placement="left"
             title="Delete Subscription"></i>
          <i className={increaseClass} onClick={this.increase}
             data-toggle="tooltip" data-placement="top"
             title="Increase Link Count"></i>
          <i className={decreaseClass} onClick={this.decrease}
             data-toggle="tooltip" data-placement="top"
             title="Decrease Link Count"></i>
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
    var hasPreferences = preferenceNodes.length != 0;
    return (
      <div className="prefernces-list">
        <table className="table">
          <thead>
            <th>Subreddit</th>
            <th>Count</th>
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

var PreferenceInsertForm = React.createClass({
  insertSubscription: function() {
    var subreddit = $("#subreddit");
    var count = $("#linkcount option:selected").val();

    if (!subreddit.val().startsWith("/r/")) {
      alert("Subreddit should start with /r/");
      subreddit.val("");
      subreddit.focus();
      return
    }

    if (count==0) {
      alert("You should set the link count");
      return
    }

    var new_data = this.props.data;
    var all_subreddits = this.props.subreddits;

    var found = $.inArray(subreddit.val(), all_subreddits) > -1;
    if(!found) {
      alert("We are currently only allowing predefined subreddits. Sorry");
      return
    }

    new_data.unshift({"subreddit": subreddit.val(), "count": Number(count)});
    this.props.saveData(new_data);
    subreddit.val("");
  },
  totalCounts: function() {
    var totalLinkCount = 0;
    var totalSubredditCount = 0;
    this.props.data.map(function(pref) {
      totalLinkCount += Number(pref.count);
      totalSubredditCount += 1;
    });
    var out = {
      "totalLink": Number(totalLinkCount),
      "totalSubreddits": Number(totalSubredditCount)
    };
    return out;
  },
  render: function() {
    var counts = this.totalCounts();
    return (
      <div className="row preference-form">
        <div className="col-lg-6">
          <table className="table">
            <thead>
              <th colSpan={2}>Subreddit Insertion</th>
            </thead>
            <tbody>
              <tr>
                <td>Subreddit</td>
                <td>
                  <input type="text" className="form-control typeahead"
                         id="subreddit" placeholder="/r/example" />
                </td>
              </tr>
              <tr>
                <td>Link Count</td>
                <td>
                  <select id="linkcount" className="form-control select-box">
                    <option value={0}>Link Count</option>
                    <option value={1}>1</option>
                    <option value={2}>2</option>
                    <option value={3}>3</option>
                    <option value={4}>4</option>
                    <option value={5}>5</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td colSpan={2}>
                  <button className="btn btn-default" role="button"
                          onClick={this.insertSubscription}>
                    <i className="fa fa-plus"></i> Insert New Subscription
                  </button>
                </td>
              </tr>
            </tbody>


          </table>


        </div>

        <div className="col-lg-6">
          <table className="table">
            <thead>
              <th colSpan={2}>Membership Info</th>
            </thead>
            <tbody>
              <tr>
                <td>Total Links</td>
                <td>{counts.totalLink}</td>
              </tr>
              <tr>
                <td>Total Subreddits</td>
                <td>{counts.totalSubreddits}</td>
              </tr>
              <tr>
                <td colSpan={2}>{this.props.member.email}</td>
              </tr>
            </tbody>
          </table>
        </div>
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
    var url = location.origin + location.pathname + "/json/" + location.search;
    console.log("data to be saved");
    this.setState({data: data});
    var d = JSON.stringify(data);
    console.log(d);

    $.ajax({
      type: "POST",
      url: url,
      data: d,
      dataType: "json",
      contentType: "application/json"
    });

  },
  getInitialState: function() {
    return {data: [], subreddits: []};
  },
  getSubredditList: function() {
    $.ajax({
      url: "/subs/subreddits/json/",
      dataType: 'json',
      cache: false,
      success: function(response) {
        this.setState({subreddits: response["subreddits"]});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function() {
    this.getDataFromServer();
    this.getSubredditList();
  },
  componentDidUpdate: function() {
    $('[data-toggle="tooltip"]').tooltip();
  },
  render: function() {
    var panelClassName = "panel panel-default";
    if(this.state.data.length == 0) {
      panelClassName = "panel panel-default empty";
    } else {
      panelClassName = "panel panel-default";
    }
    return (
      <div className="prefrences-box">
        <div className="panel panel-default">
          <div className="panel-heading">
            New Subscription
          </div>
          <div className="panel-body">
            <PreferenceInsertForm data={this.state.data}
                                  member={this.props.member}
                                  subreddits={this.state.subreddits}
                                  saveData={this.saveDataToServer} />
          </div>
        </div>

        <div className={panelClassName}>
          <div className="panel-heading">
            Manage Subscriptions
          </div>
          <div className="panel-body">
            <PreferencesList data={this.state.data} saveData={this.saveDataToServer} />
          </div>
        </div>
      </div>
    );
  }
});


React.render(
  <PreferencesBox member={member}/>,
  document.getElementById('react-container')
);
