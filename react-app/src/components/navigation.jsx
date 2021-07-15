import React from "react";
import "./navigation.css";
import AnchorButton from "./anchorButton";

class Navigation extends React.Component {
  state = {
    targets: [
      {
        name: "Home",
        page: "home",
      },
      {
        name: "Search",
        page: "search",
      },
    ],
  };

  render() {
    return (
      <nav>
        <span className="site_title">Tag Linter</span>
        <ul className="navigation_entry_list">
          {this.state.targets.map((target) => (
            <li
              className="navigation_entry"
              key={target.key || "nav-entry-" + target.page}
            >
              <AnchorButton
                onClick={() => this.props.setPageFunc(target.page)}
                buttonText={target.name}
              ></AnchorButton>
            </li>
          ))}
        </ul>
      </nav>
    );
  }
}

export default Navigation;
