import React from "react";

import "./anchorButton.css";

import "../icons.css";

class AnchorButton extends React.Component {
  render() {
    var spanClassName = this.props.spanClassName || "";

    if (this.props.icon != null) {
      var left = (this.props.iconLeft || "true") === "true";

      if (left) {
        spanClassName += "icon_left icon_left_" + this.props.icon;
      } else {
        spanClassName += "icon_right icon_right_" + this.props.icon;
      }
    }

    return (
      <button className="anchorbutton" onClick={this.props.onClick}>
        <span style={this.props.spanStyle} className={spanClassName}>
          {this.props.buttonText}
        </span>
        {this.props.children}
      </button>
    );
  }
}

export default AnchorButton;
