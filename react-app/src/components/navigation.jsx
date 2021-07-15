import React from "react";
import "./navigation.css";

class NavigationEntry extends React.Component {
  render() {
    return <li className="navigation_entry">{this.props.name}</li>;
  }
}

class Navigation extends React.Component {
  state = {
    targets: [
      {
        id: "target-home",
        name: "Home",
      },
      {
        id: "target-search",
        name: "Search",
      },
    ],
  };

  render() {
    return (
      <nav>
        <span class="site_title">Tag Linter</span>
        <ul className="navigation_entry_list">
          {this.state.targets.map((target) => (
            <NavigationEntry key={target.id} name={target.name} />
          ))}
        </ul>
      </nav>
    );
  }
}

export default Navigation;
