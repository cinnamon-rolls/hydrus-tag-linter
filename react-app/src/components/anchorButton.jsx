import React from "react";

import "./anchorButton.css";

class AnchorButton extends React.Component {
  render() {
    return (
      <button
        onClick={this.props.onClick}
        className="anchorbutton"
      >
        <span>{this.props.buttonText}</span>
        {this.props.children}
      </button>
    );
  }
}

export default AnchorButton;
