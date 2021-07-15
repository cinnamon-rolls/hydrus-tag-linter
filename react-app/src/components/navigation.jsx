import React from "react";

class NavigationEntry extends React.Component {
  render() {
    return <li>{this.props.name}</li>;
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
      }
    ],
  };

  render() {
    return (
      <nav>
        <span class="site-title">Tag Linter</span>
        <ul>
          {this.state.targets.map((target) => (
            <NavigationEntry key={target.id} name={target.name} />
          ))}
        </ul>
      </nav>
    );
  }
}

export default Navigation;
