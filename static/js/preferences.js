var urlParam = function (name) {
  if(name=(new RegExp('[?&]' + encodeURIComponent(name) + '=([^&]*)')).exec(location.search))
    return decodeURIComponent(name[1]);
}

if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.slice(0, str.length) == str;
  };
}

var Preference = React.createClass({displayName: "Preference",
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
      React.createElement("tr", null, 
        React.createElement("td", null, this.props.subreddit), 
        React.createElement("td", null, this.props.count), 
        React.createElement("td", null, 
          React.createElement("i", {className: deleteClass, onClick: this.deleteThis, 
             "data-toggle": "tooltip", "data-placement": "left", title: "Delete Subscription"}), 
          React.createElement("i", {className: increaseClass, onClick: this.increase}), 
          React.createElement("i", {className: decreaseClass, onClick: this.decrease})
        )
      )
    )
  }
});

var PreferencesList = React.createClass({displayName: "PreferencesList",
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
        React.createElement(Preference, {subreddit: pref.subreddit, count: pref.count, 
                    update: updateData})
      );
    });
    var hasPreferences = preferenceNodes.length != 0;
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

var PreferenceInsertForm = React.createClass({displayName: "PreferenceInsertForm",
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
    new_data.unshift({"subreddit": subreddit.val(), "count": count});
    this.props.saveData(new_data);

    subreddit.val("");
  },
  render: function() {
    return (
      React.createElement("div", {className: "row preference-form"}, 
        React.createElement("div", {className: "col-xs-12"}, 
          React.createElement("input", {type: "text", className: "form-control typeahead", 
                 id: "subreddit", placeholder: "Subreddit: /r/example"}), 

          React.createElement("select", {id: "linkcount", className: "form-control select-box"}, 
            React.createElement("option", {value: 0}, "Link Count"), 
            React.createElement("option", {value: 1}, "1"), 
            React.createElement("option", {value: 2}, "2"), 
            React.createElement("option", {value: 3}, "3"), 
            React.createElement("option", {value: 4}, "4"), 
            React.createElement("option", {value: 5}, "5")
          ), 

          React.createElement("button", {className: "btn btn-default", role: "button", 
             onClick: this.insertSubscription}, 
            React.createElement("i", {className: "fa fa-plus"}), " Insert New Subscription"
          )
        )

      )
    )
  }
});

var PreferencesBox = React.createClass({displayName: "PreferencesBox",
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
    var panelClassName = "panel panel-default";
    if(this.state.data.length == 0) {
      panelClassName = "panel panel-default empty";
    } else {
      panelClassName = "panel panel-default";
    }

    return (
      React.createElement("div", {className: "prefrences-box"}, 
        React.createElement("div", {className: "panel panel-default"}, 
          React.createElement("div", {className: "panel-heading"}, 
            "New Subscription"
          ), 
          React.createElement("div", {className: "panel-body"}, 
            React.createElement(PreferenceInsertForm, {data: this.state.data, saveData: this.saveDataToServer})
          )
        ), 

        React.createElement("div", {className: panelClassName}, 
          React.createElement("div", {className: "panel-heading"}, 
            "Manage Subscriptions"
          ), 
          React.createElement("div", {className: "panel-body"}, 
            React.createElement(PreferencesList, {data: this.state.data, saveData: this.saveDataToServer})
          )
        )
      )
    );
  }
});


React.render(
  React.createElement(PreferencesBox, null),
  document.getElementById('react-container')
);
