import React from "react";
import "./navigation.css";
import AnchorButton from "./anchorButton";

class Navigation extends React.Component {
  state = {
    targets: [
      {
        id: "target-home",
        name: "Home",
        page: "home",
      },
      {
        id: "target-search",
        name: "Search",
        page: "search",
      },
    ],
  };

  render() {
    return (
      <nav>
        <span class="site_title">Tag Linter</span>
        <ul className="navigation_entry_list">
          {this.state.targets.map((target) => (
            <li className="navigation_entry">
              <AnchorButton
                key={target.id}
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
