import React from "react";

import "./thumbnail.css";

import { getThumbnailUrl } from "./apiHelper";

class Thumbnail extends React.Component {
  render() {
    var fileID = this.props.fileID;

    if (fileID == null) {
      return <span>ERROR: No fileID set</span>;
    }

    var onClick;

    if (this.props.onClick != null) {
      onClick = this.props.onClick;
    } else if (this.props.appBinds != null) {
      onClick = () => this.props.appBinds.viewFile(fileID);
    } else {
      onClick = () => {
        return;
      };
    }

    return (
      <div className="thumbnail" onClick={onClick}>
        <img src={getThumbnailUrl(fileID)} alt={"Thumbnail #" + fileID} />
      </div>
    );
  }
}

export default Thumbnail;
