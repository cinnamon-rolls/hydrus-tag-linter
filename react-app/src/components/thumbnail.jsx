import React from "react";

import "./thumbnail.css";

import { getThumbnailUrl } from "./apiHelper";

class Thumbnail extends React.Component {
  render() {
    var fileID = this.props.fileID;

    if (fileID == null) {
      return <span>ERROR: No fileID set</span>;
    }

    return (
      <div className="thumbnail">
        <img src={getThumbnailUrl(fileID)} alt={"Thumbnail #" + fileID} />
      </div>
    );
  }
}

export default Thumbnail;
